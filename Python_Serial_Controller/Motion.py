import serial

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
                self.cSer = serial.Serial(port='/dev/ttyACM0', baudrate=9600)     


	def cBackLeftWheelSend(self, aRecievedSpeed):
		cBackLeftWheel = aRecievedSpeed
                cSer.send(cBackLeftWheel)

	def cBackRightWheelSend(self, aRecievedSpeed):
		cBackRightWheel = aRecievedSpeed
                cSer.send(cBackRightWheel)

	def cFrontLeftWheelSend(self, aRecievedSpeed):
		cFrontLeftWheel = aRecievedSpeed
                cSer.send(cFrontLeftWheel)

	def cFrontRightWheelSend(self, aRecievedSpeed):
		cFrontRightWheel = aRecievedSpeed
                cSer.send(cFrontRightWheel)

	def cBucketMotorSend(self, aRecievedSpeed):
		cBucketMotor = aRecievedSpeed
                cSer.send(cBucketMotor)

	def cConveryerMotorSend(self, aRecievedSpeed):
		cConveryerMotor = aRecievedSpeed
                cSer.send(cConveryerMotor)

	def cSteeringActSend(self, aRecievedSpeed):
		cSteeringAct = aRecievedSpeed
                cSer.send(cSteeringAct)

	def cBucketActSend(self, aRecievedSpeed):
		cBucketAct = aRecievedSpeed
                cSer.send(cBucketAct)
