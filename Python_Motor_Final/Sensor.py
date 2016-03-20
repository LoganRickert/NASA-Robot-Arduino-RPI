
import serial
from threading import lock

# sensor class
class Sensor:

    # define variables
    def __init__(self):
        self.cBackLeftWheelEncoder = 0
        self.cBackRightWheelEncoder = 0
        self.cFrontLeftWheelEncoder = 0
        self.cFrontRightWheelEncoder = 0
        self.cSteeringActSensor = 0
        self.cBucketActSensor = 0
        self.cIRBack = 0

    def cBackLeftWheelEncoderRead(self, lock, aSer):
        lock.acquire()
        aSer.write('J0\n')
        cBackLeftWheelEncoder = aSer.readline()[1:-1]
        lock.release()

    def cBackRightWheelEncoderRead(self, lock, aSer):
        lock.acquire()
        aSer.write('K0\n')
        cBackRightWheelEncoder = aSer.readline()[1:-1]
        lock.release()

    def cFrontLeftWheelEncoderRead(self, lock, aSer):
        lock.acquire()
        aSer.write('L0\n')
        cFrontLeftWheelEncoder = aSer.readline()[1:-1]
        lock.release()

    def cFrontRightWheelEncoderRead(self, lock, aSer):
        lock.acquire()
        aSer.write('M0\n')
        cFrontRightWheelEncoder = aSer.readline()[1:-1]
        lock.release()

    def cSteeringActSensorRead(self, lock, aSer):
        lock.acquire()
        aSer.write('N0\n')
        cSteeringActSensor = aSer.readline()[1:-1]
        lock.release()

    def cBucketActSensorRead(self, lock, aSer):
        lock.acquire()
        aSer.write('O0\n')
        cSteeringActSensor = aSer.readline()[1:-1]
        lock.release()

    def cIRBack(self, lock, aSer):
        lock.acquire()
        aSer.write('P0\n')
        cIRBack = aSer.readline()[1:-1]
        lock.release()
