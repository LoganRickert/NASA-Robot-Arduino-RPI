
import socket
from threading import lock
import time

# import pygame
# from pygame.locals import *

def run(print_lock, serial_lock, rasp_serial, client):
    check = recv_check(print_lock, client)

    if check != "superawesomesecurepassword":
        client.close()
        return

    client.send("ready\n")

    global motion
    global sensor

    should_continue = True

    while should_continue:
        data = recvall(print_lock, client_socket)

        for item.split() in data:
            if item[1] == 'A':
                motion.cAllWheelsWrite(item[1:])
            if item[1] == 'B':
                motion.cBackLeftWheelWrite(item[1:])
            if item[1] == 'C':
                motion.cBackRightWheelWrite(item[1:])
            if item[1] == 'D':
                motion.cFrontLeftWheelWrite(item[1:])
            if item[1] == 'E':
                motion.cFrontRightWheelWrite(item[1:])
            if item[1] == 'F':
                motion.cBucketMotorWrite(item[1:])
            if item[1] == 'G':
                motion.cConveryerMotorWrite(item[1:])
            if item[1] == 'H':
                motion.cSteeringActWrite(item[1:])
            if item[1] == 'I':
                motion.cBucketActWrite(item[1:])

            if item[1] == 'J':
                return Sensor.cBackLeftWheelEncoder
            if item[1] == 'K':
                return Sensor.cBackRightWheelEncoder
            if item[1] == 'L':
                return Sensor.cFrontLeftWheelEncoder
            if item[1] == 'M':
                return Sensor.cFrontRightWheelEncoder
            if item[1] == 'N':
                return Sensor.cSteeringActSensor
            if item[1] == 'O':
                return Sensor.cBucketActSensor
            if item[1] == 'P':
                return Sensor.cIRBack

            if item[1] == 'Q':
                return '-'.join(
                    Sensor.cBackLeftWheelEncoder,
                    Sensor.cBackRightWheelEncoder,
                    Sensor.cFrontLeftWheelEncoder,
                    Sensor.cFrontRightWheelEncoder,
                    Sensor.cSteeringActSensor,
                    Sensor.cBucketActSensor,
                    Sensor.cIRBack
                )

            if item[1] == 'R':
                return get_picture(item[1])

def get_picture(which_picture):
    return which_picture

def update_sensors(print_lock, aSer):
    global motion
    global sensor
    global arduino_to_write

    temp = arduino_to_write
    arduino_to_write = []

    for item in temp:
        aSer.write(item + '\n')
        aSer.flushOutput()

    sensor.update(print_lock, aSer.readline())

    # Sleep for 100 milliseconds
    time.sleep(.1);

def recvall(print_lock, client_socket):
    data = ""

    with print_lock:
        print "Recving data!"

    while data[-1] != "\n":
        packet = client_socket.recv(1024)
        data += packet

    with print_lock:
        print data.split('\n')

    return data.split('\n')

def recv_check(print_lock, client_socket):
    data = ""

    with print_lock:
        print "Checking client"

    packet = client_socket.recv(26)

    print 'Check: ', packet

    return packet

def setupSocket(lock, server_addr, server_socket):
    with lock:
        print 'Starting server on %s:%s' % server_addr

    server_socket.bind(server_addr)
    server_socket.listen(5)
