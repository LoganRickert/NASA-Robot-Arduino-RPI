
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

	def cBackLeftWheelSend(self, aRecievedSpeed):
		cBackLeftWheel = aRecievedSpeed
		# serial.send()

	def cBackRightWheelSend(self, aRecievedSpeed):
		cBackRightWheel = aRecievedSpeed
		# serial.send()

	def cFrontLeftWheelSend(self, aRecievedSpeed):
		cFrontLeftWheel = aRecievedSpeed
		# serial.send()

	def cFrontRightWheelSend(self, aRecievedSpeed):
		cFrontRightWheel = aRecievedSpeed
		# serial.send()

	def cBucketMotorSend(self, aRecievedSpeed):
		cBucketMotor = aRecievedSpeed
		# serial.send()

	def cConveryerMotorSend(self, aRecievedSpeed):
		cConveryerMotor = aRecievedSpeed
		# serial.send()

	def cSteeringActSend(self, aRecievedSpeed):
		cSteeringAct = aRecievedSpeed
		# serial.send()

	def cBucketActSend(self, aRecievedSpeed):
		cBucketAct = aRecievedSpeed
		# serial.send()
