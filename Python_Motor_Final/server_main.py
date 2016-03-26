
"""

    Serial may give back str ints instead
    of ints. Need to investage this.

"""

import serial
import socket
import time

from threading import Lock
from threading import Thread

import Motion
import Sensor
import Server
import settings

# The width of the pygame window
WIN_WIDTH = 640
WIN_HEIGHT = 480
 
# Server address
# Host:port
port = int(raw_input('port: '))
server_addr = ('', port)

def main():
    print_lock = Lock()

    socket_lock = Lock()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.setupSocket(print_lock, server_addr, server_socket)

    rasp_serial = serial.Serial(
        # port='/dev/ttyUSB0', # Linux
        port='COM7',           # Windows
        baudrate=9600,
    )

    settings.init()

    threads = []

    update_sensors_thread = Thread(
        target=Server.update_sensors,
        args=(print_lock, rasp_serial)
    )
    
    threads.append(update_sensors_thread)
    update_sensors_thread.start()

    should_continue = True

    while should_continue:
        with print_lock:
            print "Waiting for new client..."

        client, addr = server_socket.accept()

        thread = Thread(target=Server.run, args=(print_lock, client))
        threads.append(thread)
        thread.start()

    with print_lock:
        print "Joining threads."

    for thread in threads:
        thread.join()

    with print_lock:
        print "All threads closed."

if __name__ == "__main__":
    main()
