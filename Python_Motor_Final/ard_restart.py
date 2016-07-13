import serial
import time

ard = serial.Serial('/dev/ttyACM0', baudrate=9600)

time.sleep(1)

print ard.write('Z0\n')

time.sleep(1)

print ard.inWaiting()

if ard.inWaiting() > 0:
  print ard.readline()
else:
  print 'Nothing waiting'

ard.close()
