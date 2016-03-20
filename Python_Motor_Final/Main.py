# imports
import serial
import Motion.py as MotionClass
import Sensor.py as SensorClass

if __init__ == __main__:
    motors(5,5,5,5,5)    

# function to control motors
def motors(aMotorSpeed,aBucketMotor,aConveyerMotor,aLinBucket,aLinTurn):
    lMotion = MotionClass()
    lMotion.cBackLeftWheelSend(aMotorSpeed)
    lMotion.cBackRightWheelSend(aMotorSpeed)
    lMotion.cFrontLeftWheelSend(aMotorSpeed)
    lMotion.cFrontRightWheelSend(aMotorSpeed)
    lMotion.cBucketMotorSend(aBucketMotor)
    lMotion.cConveryerMotorSend(aConveyerMotor)
    lMotion.cSteeringActSend(aLinBucket)
    lMotion.cBucketActSend(aLinTurn)
    
# funtion to read sensors
def sensors():
    lSensor = SensorClass()
    blw = lSensor.cBackLeftWheelEncoderRead()
    brw = lSensor.cBackRightWheelEncoderRead()
    flw = lSensor.cFrontLeftWheelEncoderRead()
    frw = lSensor.cFrontRightWheelEncoderRead()
    sa = lSensor.cSteeringActSensorRead()
    ba = lSensor.cBucketActSensorRead()
    
    



    


    
