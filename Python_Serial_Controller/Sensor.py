
class Sensor:

	def __init__(self):
		self.cBackLeftWheelEncoder = 0
		self.cBackRightWheelEncoder = 0
		self.cFrontLeftWheelEncoder = 0
		self.cFrontRightWheelEncoder = 0
		self.cSteeringActSensor = 0
		self.cBucketActSensor = 0
		cIR = 0

	def getRead(self):
		data = 0 # getReadFromRPI()
		self.cBackLeftWheelEncoder = data[0]
		self.cBackRightWheelEncoder = data[1]
		self.cFrontLeftWheelEncoder = data[2]
		self.cFrontRightWheelEncoder = data[3]
		self.cSteeringActSensor = data[4]
		self.cBucketActSensor = data[5]
		self.cIR = data[6]
