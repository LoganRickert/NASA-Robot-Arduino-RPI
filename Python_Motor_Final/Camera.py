import pygame
import pygame.camera
from pygame.locals import *
import cv2
import bz2

import numpy

import time

def _calc_pixel_color(current_color):
    new_val = ((((((current_color >> 16) & 0xff)*76) + (((current_color >> 8) & 0xff)*150) + \
        ((current_color & 0xff)*29)) >> 8))

    div = 8
    color = new_val / div

    return color

_calc_pixel_color = numpy.vectorize(_calc_pixel_color)

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
        time_start = time.time()

        self.camera.start()
        
        tempSurface = pygame.surface.Surface(self.size, 0, self.display)
        tempSurface = self.camera.get_image(tempSurface)


        self.camera.stop()

        wentThrough = 0

        pixels = []

        pxarrayA = pygame.PixelArray(tempSurface)[0::4, 0::4]
        pxarrayB = pygame.PixelArray(self.snapshot)[0::4, 0::4]

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
                pxarrayB[x, y] = (color * div, color * div, color * div)

        del pxarrayA
        del pxarrayB

        print "Took:", (time.time() - time_start)

        # print "Went through:", self.compress(pixels)

        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()

    def compress(self, pixels):
        time_start = time.time()
        compresseda = bz2.compress(''.join(str(pixels)), 9)
        print "C took:", (time.time() - time_start)
        print 'new lista length:', len(compresseda) * 8
        
        return len(compresseda)

def main():
    camera = Camera()

    while True:
        camera.get_and_flip(0)
        pygame.time.wait(1000)

if __name__ == "__main__":
    main()