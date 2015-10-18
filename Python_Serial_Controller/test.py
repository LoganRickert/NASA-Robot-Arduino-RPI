import serial
import time

connection = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(3)
print("Working on it")

connection.write('3')
print connection.readline()
