import pygame
import pygame.camera
from pygame.locals import *
import cv2
import bz2

pygame.init()
pygame.camera.init()

class Capture(object):
    def __init__(self):
        self.size = (640, 360)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[1], self.size)
        self.cam.start()

        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

        self.count = 0
        self.ready = 0

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check 
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        self.ready += 1
        if self.cam.query_image():
            tempSurface = pygame.surface.Surface(self.size, 0, self.display)
            tempSurface = self.cam.get_image(tempSurface)

            if self.ready > 50:
                pxarrayA = pygame.PixelArray(tempSurface)
                pxarrayB = pygame.PixelArray(self.snapshot)

                wentThrough = 0

                pixels = []

                for x in range(0, 640, 4):
                    for y in range(0, 360, 4):
                        wentThrough += 1
                        col = pxarrayA[x, y]
                        new_val = ((((((col >> 16) & 0xff)*76) + (((col >> 8) & 0xff)*150) + \
                            ((col & 0xff)*29)) >> 8))

                        div = 8
                        color = new_val / div
                        pixels.append(color)
                        pxarrayB[x, y] = (color * div, color * div, color * div)

                del pxarrayA
                del pxarrayB
                print "Went through:", wentThrough, self.compress(pixels)
                self.ready = 0

        self.count += 1
        pygame.image.save(self.snapshot, "temp.jpg")

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()

    def compress(self, pixels):
        change = []

        delta = pixels[0] + 31
        change.append(1)
        change.append(delta)
        largest = 1
        largestD = delta
        lowest = delta

        for item in pixels[1:]:
            now = pixels[-1] - item + 31

            if now == change[-1]:
                if change[-2] > 5:
                    tempb = change[-1]
                    change.append(1)
                    change.append(tempb)
                else:
                    change[-2] += 1

                if change[-2] > largest: largest = change[-2]
            else:
                change.append(1)
                change.append(now)

                delta = now
                if delta > largestD: largestD = delta
                if delta < lowest: lowest = delta

        new_list = []

        numberRange = largestD - lowest

        print 'largest:', largest
        print 'largestD:', largestD
        print 'lowest:', lowest
        print 'delta:', numberRange
        print 'Change length:', len(change)
        compresseda = bz2.compress(''.join(str(pixels)), 9)
        compressedb = bz2.compress(''.join(str(change)), 9)
        print 'new lista length:', len(compresseda) * 8
        print 'new listb length:', len(compressedb) * 8

        return len(change)

    def main(self):
        going = True
        while going:
            pygame.time.wait(20)
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False

            self.get_and_flip()

capture = Capture()
capture.main()
