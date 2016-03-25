
import socket
import time
from threading import Thread

import pygame
from pygame.locals import *

import Motion
import Sensor

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('', 1337))
    client.send('superawesomesecurepassword\n')

    should_continue = True

    while should_continue:
        console = raw_input('> ')
        client.send(console + '\n')

        if console[0] in 'JKLMNOPQ':
            print 'Got back:', client.recvall(client)

def recvall(client_socket):
    data = ""

    with print_lock:
        print "Recving data!"

    while data[-1] != "\n":
        packet = client_socket.recv(1024)
        data += packet

    with print_lock:
        print data.split('\n')

    return data.split('\n')

if __name__ == "__main__":
    main()
