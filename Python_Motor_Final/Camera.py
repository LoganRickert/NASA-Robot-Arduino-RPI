import pygame
import pygame.camera
from pygame.locals import *
import bz2

import time

class Camera:
    def __init__(self):
        self.size = (640, 360)

        pygame.init()
        pygame.camera.init()

        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        # print "Camera list:", self.clist

        self.cameras = []
        self.current_images = []

        if not self.clist:
            self.total_cameras = 0
            print "NO CAMERAS WERE DETECTED!"
        else:
            for camera in self.clist:
                self.cameras.append(pygame.camera.Camera(camera, self.size))
                self.current_images.append(["", time.time()])

            # create a surface to capture to.  for performance purposes
            # bit depth is the same as that of the display surface.
            self.snapshot = pygame.surface.Surface(self.size, 0, self.display)


    def get_image(self, camera_number):
        #if self.camera.query_image():
        # time_start = time.time()

        if camera_number >= len(self.cameras):
            print "CAMERA OUT OF BOUNCE"
            return 0

        if time.time() - self.current_images[camera_number][1] < 1:
            return self.current_images[camera_number][0]

        self.cameras[camera_number].start()
        
        tempSurface = pygame.surface.Surface(self.size, 0, self.display)
        tempSurface = self.cameras[camera_number].get_image(tempSurface)

        self.cameras[camera_number].stop()

        wentThrough = 0

        pixels = []

        pxarrayA = pygame.PixelArray(tempSurface)[0::4, 0::3]
        # pxarrayB = pygame.PixelArray(self.snapshot)[0::4, 0::3]

        lenx = len(pxarrayA)
        leny = len(pxarrayA[0])

        # _calc_pixel_color(pxarrayA)

        for x in range(0, lenx):
            for y in range(0, leny):
                col = pxarrayA[x, y]
                new_val = ((((((col >> 16) & 0xff)*76) + (((col >> 8) & 0xff)*150) + \
                    ((col & 0xff)*29)) >> 8))

                div = 8
                color = new_val / div
                pixels.append(color)
                # pxarrayB[x, y] = (color * div, color * div, color * div)

        del pxarrayA
        # del pxarrayB

        # print "Took:", (time.time() - time_start)

        self.current_images[camera_number] = [self._compress(pixels), time.time()]
        return self.current_images[camera_number][0]

        # self.display.blit(self.snapshot, (0,0))
        # pygame.display.flip()

    def _compress(self, pixels):
        time_start = time.time()
        compresseda = bz2.compress(''.join(str(pixels)), 9)
        # print "C took:", (time.time() - time_start)
        # print 'new lista length:', len(compresseda) * 8
        return compresseda.encode('ascii')

def main():
    camera = Camera()

    while True:
        camera.get_and_flip(0)
        pygame.time.wait(1000)

if __name__ == "__main__":
    main()