
import socket
import time
from threading import Thread

import pygame
from pygame.locals import *

import Motion
import Sensor

import bz2
import binascii
import ast

size = (640, 360)

x_scale = 4
y_scale = 3

pygame.init()
display = pygame.display.set_mode(size)
snapshot = pygame.surface.Surface(size, 0, display)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('10.1.110.99', 1338))
    client.send('superawesomesecurepassword\n')

    print recvall(client)

    should_continue = True

    """
    while should_continue:
        current = time.time()
        client.send('R0\n')
        temp = ''.join(recvall(client))
        print "Time:                            ", time.time() - current
        current = time.time()
        image = bz2.decompress(binascii.unhexlify(temp))
        print "sent:", len(temp)
        print "comp:", len(binascii.unhexlify(temp))
        print "pixels:", len(image)
        image = ast.literal_eval(image)

        tempSurface = pygame.surface.Surface(size, 0, display)
        pxarrayA = pygame.PixelArray(snapshot)

        lenx = len(pxarrayA)
        leny = len(pxarrayA[0])

        print 'lenx:', lenx
        print 'leny:', leny

        color_end = []

        for x in range(0, lenx):
            current_color = []
            for y in range(0, leny):
                money_shot = (leny / y_scale) * (x / x_scale) + (y / y_scale)
                if (money_shot) < len(image):
                    color = image[money_shot]
                    div = 8
                    pxarrayA[x, y] = (color * div, color * div, color * div)

        del pxarrayA

        print "Flipping surface"
        display.fill((255, 255, 255))
        print "Blitzing"
        display.blit(snapshot, (0,0))
        print "Flipping"
        pygame.display.flip()
        print "Waiting"
        # pygame.event.wait()
        print "Done                     +", time.time() - current
        print "Done."
    """
    
    while should_continue:
        console = raw_input('> ')
        client.send(console + '\n')

        if console[0] in 'JKLMNOPQ':
            print 'Got back:', recvall(client)

        if console[0] == 'R':
            current = time.time()
            temp = ''.join(recvall(client))
            print time.time() - current
            image = bz2.decompress(binascii.unhexlify(temp))
            print "sent:", len(temp)
            print "comp:", len(binascii.unhexlify(temp))
            print "pixels:", len(image)
            image = ast.literal_eval(image)

            tempSurface = pygame.surface.Surface(size, 0, display)
            pxarrayA = pygame.PixelArray(snapshot)

            lenx = len(pxarrayA)
            leny = len(pxarrayA[0])

            print 'lenx:', lenx
            print 'leny:', leny

            color_end = []

            for x in range(0, lenx):
                current_color = []
                for y in range(0, leny):
                    money_shot = (leny / y_scale) * (x / x_scale) + (y / y_scale)
                    if (money_shot) < len(image):
                        color = image[money_shot]
                        div = 8
                        pxarrayA[x, y] = (color * div, color * div, color * div)

            del pxarrayA

            print "Flipping surface"
            display.fill((255, 255, 255))
            display.blit(snapshot, (0,0))
            pygame.display.flip()
            pygame.event.wait()

        if console == 'quit':
            should_continue = False
            client.close()

def recvall(client_socket):
    data = "z"
    
    print "Recving data!"

    while data[-1] != "\n":
        packet = client_socket.recv(1024)
        data += packet

    data = data[1:] # We need the z so we can check data[-1]
                    # It will give out of bounce error otherwise.

    # print 'Recving:', data.split('\n')[:-1]

    return data.split('\n')[:-1]

if __name__ == "__main__":
    main()
