
import socket
from threading import Lock
import time
import settings

import binascii

# import pygame
# from pygame.locals import *

def run(print_lock, client_socket):
    check = recv_check(print_lock, client_socket)

    if check != "superawesomesecurepassword":
        with print_lock:
            print "Not right password!"
        client_socket.close()
        return

    client_socket.send("ready\n")

    should_continue = True

    while should_continue:
        data = recvall(print_lock, client_socket)

        for item in data:
            if len(item) < 1: continue

            with print_lock:
                print "Processing:", item

            if item[0] == 'A':
                settings.settings.motion.cAllWheelsWrite(item[1:])
            if item[0] == 'B':
                settings.motion.cBackLeftWheelWrite(item[1:])
            if item[0] == 'C':
                settings.motion.cBackRightWheelWrite(item[1:])
            if item[0] == 'D':
                settings.motion.cFrontLeftWheelWrite(item[1:])
            if item[0] == 'E':
                settings.motion.cFrontRightWheelWrite(item[1:])
            if item[0] == 'F':
                settings.motion.cBucketMotorWrite(item[1:])
            if item[0] == 'G':
                settings.motion.cConveryerMotorWrite(item[1:])
            if item[0] == 'H':
                settings.motion.cSteeringActWrite(item[1:])
            if item[0] == 'I':
                settings.motion.cBucketActWrite(item[1:])

            if item[0] == 'J':
                client_socket.send(str(settings.sensor.cBackLeftWheelEncoder) + '\n')
            if item[0] == 'K':
                client_socket.send(str(settings.sensor.cBackRightWheelEncoder) + '\n')
            if item[0] == 'L':
                client_socket.send(str(settings.sensor.cFrontLeftWheelEncoder) + '\n')
            if item[0] == 'M':
                client_socket.send(str(settings.sensor.cFrontRightWheelEncoder) + '\n')
            if item[0] == 'N':
                client_socket.send(str(settings.sensor.cSteeringActSensor) + '\n')
            if item[0] == 'O':
                client_socket.send(str(settings.sensor.cBucketActSensor) + '\n')
            if item[0] == 'P':
                client_socket.send(str(settings.sensor.cIRBack) + '\n')

            if item[0] == 'Q':
                client_socket.send('-'.join([
                    settings.sensor.cBackLeftWheelEncoder,
                    settings.sensor.cBackRightWheelEncoder,
                    settings.sensor.cFrontLeftWheelEncoder,
                    settings.sensor.cFrontRightWheelEncoder,
                    settings.sensor.cSteeringActSensor,
                    settings.sensor.cBucketActSensor,
                    settings.sensor.cIRBack
                ]) + '\n')

            if item[0] == 'R':
                to_send = binascii.hexlify(get_picture(int(item[1])))
                print "sent:", to_send
                client_socket.send(to_send + '\n')

def get_picture(which_picture):
    return settings.camera.get_image(which_picture)

def update_sensors(print_lock, aSer):
    while True:
        temp = settings.arduino_to_write
        settings.arduino_to_write = []

        for item in temp:
            aSer.write(item + '\n')
            aSer.flushOutput()

        settings.sensor.update(print_lock, aSer.readline())

        # Sleep for 100 milliseconds
        time.sleep(.5);

def recvall(print_lock, client_socket):
    data = "z"

    with print_lock:
        print "Recving data!"

    while data[-1] != "\n":
        packet = client_socket.recv(1024)
        data += packet

    data = data[1:] # We need the z so we can check data[-1]
                    # It will give out of bounce error otherwise.

    with print_lock:
        print data.split('\n')[:-1]

    return data.split('\n')[:-1]

def recv_check(print_lock, client_socket):
    data = ""

    with print_lock:
        print "Checking client"

    packet = client_socket.recv(26)

    with print_lock:
        print 'Check: ', packet

    return packet

def setupSocket(print_lock, server_addr, server_socket):
    with print_lock:
        print 'Starting server on %s:%s' % server_addr

    server_socket.bind(server_addr)
    server_socket.listen(5)
