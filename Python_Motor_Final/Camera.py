import pygame
import pygame.camera
from pygame.locals import *
import cv2
import bz2

class Camera:
    def __init__(self):
        self.size = (640, 360)

        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        print "Camera list:", self.clist

        if not self.clist:
            self.total_cameras = 0
            print "NO CAMERAS WERE DETECTED!"
        else:
            self.camera = pygame.camera.Camera(self.clist[1], self.size)
            self.camera.start()

            # create a surface to capture to.  for performance purposes
            # bit depth is the same as that of the display surface.
            self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self, camera):
        if self.camera.query_image():
            tempSurface = pygame.surface.Surface(self.size, 0, self.display)
            tempSurface = self.camera.get_image(tempSurface)

            # Process

        self.display.blit(self.snapshot, (0,0))
        pygame.display.flip()

def main(self):
    camera = Camera()

    while True:
        camera.get_and_flip()
        pygame.time.wait(100)

if __name__ == "__main__":
    main()