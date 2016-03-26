import pygame
import pygame.camera
from pygame.locals import *
import cv2
import bz2

class Camera:
    def __init__(self):
        self.size = (640, 360)

        pygame.init()
        pygame.camera.init()

        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        print "Camera list:", self.clist

        if not self.clist:
            self.total_cameras = 0
            print "NO CAMERAS WERE DETECTED!"
        else:
            self.camera = pygame.camera.Camera(self.clist[0], self.size)

            # create a surface to capture to.  for performance purposes
            # bit depth is the same as that of the display surface.
            self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self, camera):
        #if self.camera.query_image():
        self.camera.start()
        
        tempSurface = pygame.surface.Surface(self.size, 0, self.display)
        tempSurface = self.camera.get_image(tempSurface)

        pxarrayA = pygame.PixelArray(tempSurface)
        pxarrayB = pygame.PixelArray(self.snapshot)

        self.camera.stop()

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

def main():
    camera = Camera()

    while True:
        camera.get_and_flip(0)
        pygame.time.wait(1000)

if __name__ == "__main__":
    main()