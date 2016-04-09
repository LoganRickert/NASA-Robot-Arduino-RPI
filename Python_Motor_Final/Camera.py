import pygame
import pygame.camera
from pygame.locals import *
import bz2
import itertools

import time

# 3rd pixel..
x_scale = 3
y_scale = 3


class Camera:

    #size of the screen to display
    def __init__(self):
        #640 by 360 scree size
        self.size = (640, 360)

        # initialize pygame
        pygame.init()

        # initial pygame camera
        pygame.camera.init()

        # dispalys screen
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        
        # list of all cameras --- location of cameras
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
       
        # print "Camera list:", self.clist

        # define camera array --- object of camera
        self.cameras = []

        # define camera array --- images of camera
        self.current_images = []

        # if no cameras are connected
        if not self.clist:
            # 0 cameras
            self.total_cameras = 0
            print "NO CAMERAS WERE DETECTED!"
       
    else:
        # for each camera
        for camera in self.clist:
            # append camera objects to camera list
            self.cameras.append(pygame.camera.Camera(camera, self.size))
            # append immage and when it was taken
            self.current_images.append(["", time.time()])

            # create a surface to capture to.  for performance purposes
            # bit depth is the same as that of the display surface.
            # create the surface once, rather than each time we take an image
            self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    
    # convert color --- magic make it a 8 bit black and white pixel
    def color_convert(self, col):
       
        # shift the hexidecimal numbers around 
        new_val = ((((((col >> 16) & 0xff)*76) + (((col >> 8) & 0xff)*150) + \
                    ((col & 0xff)*29)) >> 8))
        
        div = 8
        return new_val / 8

    # retunrs the image 
    def get_image(self, camera_number):
        #if self.camera.query_image():
        time_start = time.time()

        # if camera number is > camera array list
        if camera_number >= len(self.cameras):
            print "CAMERA OUT OF BOUNCE"
            return 0

        # if time.time() - self.current_images[camera_number][1] < 1:
            # return self.current_images[camera_number][0]

        # start camera
        self.cameras[camera_number].start()
        
        # makes temp surface 
        tempSurface = pygame.surface.Surface(self.size, 0, self.display)
       
        # save camera immage (full color) to temp surfcae 
        tempSurface = self.cameras[camera_number].get_image(tempSurface)

        # stope camera
        self.cameras[camera_number].stop()

        # iterations it want through
        wentThrough = 0

        # define pixels array
        pixels = []

        # make pixel array of the temp surface that has picture (full color)
        pxarrayA = pygame.PixelArray(tempSurface)#[0::4, 0::3]

        # make a pixel of array of what will be the manipulated  pixels
        pxarrayB = pygame.PixelArray(self.snapshot)#[0::4, 0::3]

        # makes a single array from the array of array's that pygame
        # natively returns
        # temp1 = list(itertools.chain(*pxarrayB[0::3, 0::3]))
        
        # creates applys the magic function to the single arrya made form 
        # the pxarrayB 
        #temp2 = map(self.color_convert, temp1)

        # length of array of arrays
        lenx = len(pxarrayA)

        # length of an array inside the array
        leny = len(pxarrayA[0])

        # _calc_pixel_color(pxarrayA)

        # for each array insing the array conatining arrays
        # to the length of the array containing arrays by the scale (current 3)
        for x in range(0, lenx, x_scale):
            current_color = [] #<-- ignor for now
    
        # for each pixel in arrays inside of array containing array
        for y in range(0, leny, y_scale):

        # fill in the pixelArray A[x,y]
                col = pxarrayA[x, y]

        # magic (same as magic function)
                new_val = ((((((col >> 16) & 0xff)*76) + (((col >> 8) & 0xff)*150) + \
                    ((col & 0xff)*29)) >> 8))

                div = 8
                color = new_val / div
        
        # appends color to pixels array (the array we send)
                pixels.append(color)

        # copys the new color part onto this display
                pxarrayB[x, y] = (color * div, color * div, color * div)

        # delete
        del pxarrayA
        del pxarrayB

    
        print "img_buffering:", (time.time() - time_start)

        #print 'one', sum(temp2)
        #print 'two', sum(pixels)

        # compresses the pixel array
        self.current_images[camera_number] = [self._compress(pixels), time.time()]
        
        print "total Took:", (time.time() - time_start)

        # dispalys the snap shot to the screen (hardware function)
        self.display.blit(self.snapshot, (0,0))

        # flip the image (swtich buffer (old image to new imae))
        pygame.display.flip()

        # retursn the current compressed image list
        return self.current_images[camera_number][0]

    # compresses the array
    def _compress(self, pixels):
        time_start = time.time()
        compresseda = bz2.compress(''.join(str(pixels)), 9)
        # print "C took:", (time.time() - time_start)
        # print 'new lista length:', len(compresseda) * 8
        print "comp:", len(compresseda)
        return compresseda


def main():
    camera = Camera()

    while True:
        camera.get_image(0)
        pygame.time.wait(1000)

if __name__ == "__main__":
    main()
