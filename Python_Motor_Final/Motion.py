
import serial
from threading import lock

class Motion:

    def __init__(self):
        self.cBackLeftWheel = 0
        self.cBackRightWheel = 0
        self.cFrontLeftWheel = 0
        self.cFrontRightWheel = 0
        self.cBucketMotor = 0
        self.cConveryerMotor = 0
        self.cSteeringAct = 0
        self.cBucketAct = 0

    def write(self, to_write):
        global arduino_to_write

        arduino_to_write.append(to_write)

    def cAllWheelsWrite(self, aRecievedSpeed):
        if not all(x == aRecievedSpeed for x in (self.cBackLeftWheel, self.cBackRightWheel, self.cFrontLeftWheel, self.cFrontRightWheel)):
            self.cBackLeftWheel = aRecievedSpeed
            self.cBackRightWheel = aRecievedSpeed
            self.cFrontLeftWheel = aRecievedSpeed
            self.cFrontRightWheel = aRecievedSpeed
            self.write('A' + str(aRecievedSpeed))

    def cBackLeftWheelWrite(self, aRecievedSpeed):
        if self.cBackLeftWheel != aRecievedSpeed:
            self.cBackLeftWheel = aRecievedSpeed
            self.write('B' + str(aRecievedSpeed))

    def cBackRightWheelWrite(self, aRecievedSpeed):
        if self.cBackRightWheel != aRecievedSpeed:
            self.cBackRightWheel = aRecievedSpeed
            self.write('C' + str(aRecievedSpeed))

    def cFrontLeftWheelWrite(self, aRecievedSpeed):
        if self.cFrontLeftWheel != aRecievedSpeed:
            self.cFrontLeftWheel = aRecievedSpeed
            self.write('D' + str(aRecievedSpeed))

    def cFrontRightWheelWrite(self, aRecievedSpeed):
        if self.cFrontRightWheel != aRecievedSpeed:
            self.cFrontRightWheel = aRecievedSpeed
            self.write('E' + str(aRecievedSpeed))

    def cBucketMotorWrite(self, aRecievedSpeed):
        if self.cBucketMotor != aRecievedSpeed:
            self.cBucketMotor = aRecievedSpeed
            self.write('F' + str(aRecievedSpeed))

    def cConveryerMotorWrite(self, aRecievedSpeed):
        if self.cConveryerMotor != aRecievedSpeed:
            self.cConveryerMotor = aRecievedSpeed
            self.write('G' + str(aRecievedSpeed))

    def cSteeringActWrite(self, aRecievedSpeed):
        if self.cSteeringAct != aRecievedSpeed:
            self.cSteeringAct = aRecievedSpeed
            self.write('H' + str(aRecievedSpeed))

    def cBucketActWrite(self, aRecievedSpeed):
        if self.cBucketAct != aRecievedSpeed:
            self.cBucketAct = aRecievedSpeed
            self.write('I' + str(aRecievedSpeed))
