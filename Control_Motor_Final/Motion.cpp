// Ron: Class will be used for all the motion of the robot (Motion objects)

#include "Motion.h"

// Ron: Function used to drive the robot (drive wheel motors)
void Motion::cDriveWheelsWrite(int aRecieved_BLW_Speed, int aRevieved_BRW_Speed, int aRecieved_FLW_Speed, int aRecieved_FRW_Speed) {
    cBackLeftWheel.writeMicroseconds(aRecieved_BLW_Speed);
    cBackRightWheel.writeMicroseconds(aRevieved_BRW_Speed);
    cFrontLeftWheel.writeMicroseconds(aRecieved_FLW_Speed);
    cFrontRightWheel.writeMicroseconds(aRecieved_FRW_Speed);
}

// Ron: Function used to rotate the buckets (drive bucket motor)
void Motion::cDriveBucketWrite(int aRecieved_BM_Speed) {
    cBucketMotor.writeMicroseconds(aRecieved_BM_Speed);
}

// Ron: Function used to rotate the conveyer (drive conveyer motor)
void Motion::cDriveConveyerWrite(int aRecieved_CM_Speed) {
    cConveryerMotor.writeMicroseconds(aRecieved_CM_Speed);
}

// Ron: Function used to turn the robot (move linear actuator)
void Motion::cMoveSteeringWrite(int aRecieved_SA_Angle) {
    cSteeringAct.writeMicroseconds(aRecieved_SA_Angle);
}

// Ron: Function used to drop/lift the bucket system (move linear actuator)
void Motion::cMoveBucketsWrite(int aRecieved_BA_Angle) {
    cBucketAct.writeMicroseconds(aRecieved_BA_Angle);
}

// Ron: Function used to create the object (constructor)
Motion::Motion(int aPin1,int aPin2, int aPin3, int aPin4, int aPin5, int aPin6, int aPin7, int aPin8){ 
    // Ron: attach fuctinon links the servo object to pin argument
    cBackLeftWheel.attach(aPin1);
    cBackRightWheel.attach(aPin2);
    cFrontLeftWheel.attach(aPin3);
    cFrontRightWheel.attach(aPin4);
    cSteeringAct.attach(aPin5);
    cBucketAct.attach(aPin6);
    cBucketMotor.attach(aPin7);
    cConveryerMotor.attach(aPin8);   
  }
  
// Ron: Function used to destroy the object (destructor)
Motion::~Motion() {}
