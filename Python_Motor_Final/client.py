
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
pygame.init()
display = pygame.display.set_mode(size)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('10.1.117.111', 1338))
    client.send('superawesomesecurepassword\n')

    print recvall(client)

    should_continue = True

    while should_continue:
        console = raw_input('> ')
        client.send(console + '\n')

        if console[0] in 'JKLMNOPQ':
            print 'Got back:', recvall(client)

        if console[0] == 'R':
            
            temp = ''.join(recvall(client))
            image = bz2.decompress(binascii.unhexlify(temp))
            print "sent:", len(binascii.unhexlify(temp))
            print "comp:", len(image)
            image = ast.literal_eval(image)

            tempSurface = pygame.surface.Surface(size, 0, display)
            pxarrayA = pygame.PixelArray(tempSurface)

            lenx = len(pxarrayA)
            leny = len(pxarrayA[0])

            for x in range(0, lenx / 4):
                for y in range(0, leny / 3):
                    color = image[x  * (y + 1)]
                    div = 8
                    pxarrayA[x * 4, y * 3] = (color * div, color * div, color * div)

            del pxarrayA

            print "Flipping surface"
            display.fill((0,0,0))
            display.blit(tempSurface, (0,0))
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

    print 'Recving:', data.split('\n')[:-1]

    return data.split('\n')[:-1]

if __name__ == "__main__":
    main()
