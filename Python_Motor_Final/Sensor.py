
import serial
import time

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

        self.cBackLeftWheelEncoderTime = time.time()
        self.cBackRightWheelEncoderTime = time.time()
        self.cFrontLeftWheelEncoderTime = time.time()
        self.cFrontRightWheelEncoderTime = time.time()
        self.cSteeringActSensorTime = time.time()
        self.cBucketActSensorTime = time.time()
        self.cIRBackTime = time.time()

    def update(self, print_lock, information):
        information = information.split('-')
        print information

        if len(information) == 7:
            self.cBackLeftWheelEncoder = information[0]
            self.cBackRightWheelEncoder = information[1]
            self.cFrontLeftWheelEncoder = information[2]
            self.cFrontRightWheelEncoder = information[3]
            self.cSteeringActSensor = information[4]
            self.cBucketActSensor = information[5]
            self.cIRBack = information[6].split()[0] # Removes \r\n
        else:
            with print_lock:
                print "Something's gone bad with update!"
                print "Got: ", information

    # def writeread(self, serial_lock, aSer, to_write):
    #     value = None

    #     with serial_lock:
    #         aSer.write(to_write)
    #         aSer.flushOutput()
    #         value = aSer.readline()[:-1]

    #     return value

    # def cBackLeftWheelEncoderRead(self, serial_lock, aSer):
    #     if time.time() > self.cBackLeftWheelEncoderTime + 0.250:
    #         cBackLeftWheelEncoder = self.writeread(serial_lock, aSer, 'J0\n')[1:]
    #         self.cBackLeftWheelEncoderTime = time.time()

    # def cBackRightWheelEncoderRead(self, serial_lock, aSer):
    #     if time.time() > self.cBackRightWheelEncoderTime + 0.250:
    #         self.cBackRightWheelEncoder = self.writeread(serial_lock, aSer, 'K0\n')[1:]
    #         self.cBackRightWheelEncoderTime = time.time()

    # def cFrontLeftWheelEncoderRead(self, serial_lock, aSer):
    #     if time.time() > self.cFrontLeftWheelEncoderTime + 0.250:
    #         self.cFrontLeftWheelEncoder = self.writeread(serial_lock, aSer, 'L0\n')[1:]
    #         self.cFrontLeftWheelEncoderTime = time.time()

    # def cFrontRightWheelEncoderRead(self, serial_lock, aSer):
    #     if time.time() > self.cFrontRightWheelEncoderTime + 0.250:
    #         self.cFrontRightWheelEncoder = self.writeread(serial_lock, aSer, 'M0\n')[1:]
    #         self.cFrontRightWheelEncoderTime = time.time()

    # def cSteeringActSensorRead(self, serial_lock, aSer):
    #     if time.time() > self.cSteeringActSensorTime + 0.250:
    #         self.cSteeringActSensor = self.writeread(serial_lock, aSer, 'N0\n')[1:]
    #         self.cSteeringActSensorTime = time.time()

    # def cBucketActSensorRead(self, serial_lock, aSer):
    #     if time.time() > self.cBucketActSensorTime + 0.250:
    #         self.cBucketActSensor = self.writeread(serial_lock, aSer, 'O0\n')[1:]
    #         self.cBucketActSensorTime = time.time()

    # def cIRBack(self, serial_lock, aSer):
    #     if time.time() > self.cIRBackTime + 0.250:
    #         self.cIRBack = self.writeread(serial_lock, aSer, 'P0\n')[1:]
    #         self.cIRBackTime = time.time()
