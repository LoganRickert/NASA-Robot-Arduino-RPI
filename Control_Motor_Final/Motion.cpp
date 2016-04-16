
// Ron: Class will be used for all the motion of the robot (Motion objects)

#include "Motion.h"

void Motion::cDriveWheelsWrite(int aRecieved) {
    cDriveWheelsWrite(aRecieved, aRecieved, aRecieved, aRecieved);
}

// Ron: Function used to drive the robot (drive wheel motors)
void Motion::cDriveWheelsWrite(int aRecieved_BLW_Speed, int aRevieved_BRW_Speed, int aRecieved_FLW_Speed, int aRecieved_FRW_Speed) {
    cBackLeftWheelSpeed = aRecieved_BLW_Speed;
    cBackRightWheelSpeed = aRevieved_BRW_Speed;
    cFrontLeftWheelSpeed = aRecieved_FLW_Speed;
    cFrontRightWheelSpeed = aRecieved_FRW_Speed;
    cBackLeftWheel.writeMicroseconds(aRecieved_BLW_Speed);
    cBackRightWheel.writeMicroseconds(aRevieved_BRW_Speed);
    cFrontLeftWheel.writeMicroseconds(aRecieved_FLW_Speed);
    cFrontRightWheel.writeMicroseconds(aRecieved_FRW_Speed);
}

void Motion::cDriveBLWWrite(int aRecieved_BLW_Speed) {
    cBackLeftWheelSpeed = aRecieved_BLW_Speed;
    cBackLeftWheel.writeMicroseconds(aRecieved_BLW_Speed);
}

void Motion::cDriveBRWWrite(int aRevieved_BRW_Speed) {
    cBackRightWheelSpeed = aRevieved_BRW_Speed;
    cBackRightWheel.writeMicroseconds(aRevieved_BRW_Speed);
}

void Motion::cDriveFLWWrite(int aRecieved_FLW_Speed) {
    cFrontLeftWheelSpeed = aRecieved_FLW_Speed;
    cFrontLeftWheel.writeMicroseconds(aRecieved_FLW_Speed);
}

void Motion::cDriveFRWWrite(int aRecieved_FRW_Speed) {
    cFrontRightWheelSpeed = aRecieved_FRW_Speed;
    cFrontRightWheel.writeMicroseconds(aRecieved_FRW_Speed);
}

// Ron: Function used to rotate the buckets (drive bucket motor)
void Motion::cDriveBucketWrite(int aRecieved_BM_Speed) {
    cBucketMotorSpeed = aRecieved_BM_Speed;
    cBucketMotor.writeMicroseconds(aRecieved_BM_Speed);
}

// Ron: Function used to rotate the conveyer (drive conveyer motor)
void Motion::cDriveConveyerWrite(int aRecieved_CM_Speed) {
    cConveryerMotorSpeed = aRecieved_CM_Speed;
    cConveryerMotor.writeMicroseconds(aRecieved_CM_Speed);
}

// Ron: Function used to turn the robot (move linear actuator)
void Motion::cMoveSteeringWrite(int aRecieved_SA_Speed) {
    cSteeringActSpeed = aRecieved_SA_Speed;
    cSteeringAct.writeMicroseconds(aRecieved_SA_Speed);
}

// Ron: Function used to drop/lift the bucket system (move linear actuator)
void Motion::cMoveBucketsWrite(int aRecieved_BA_Speed) {
    cBucketActSpeed = aRecieved_BA_Speed;
    cBucketAct.writeMicroseconds(aRecieved_BA_Speed);
}

int Motion::getBackLeftWheelSpeed() {
    return cBackLeftWheelSpeed;
}

int Motion::getBackRightWheelSpeed() {
    return cBackRightWheelSpeed;
}

int Motion::getFrontLeftWheelSpeed() {
    return cFrontLeftWheelSpeed;
}

int Motion::getFrontRightWheelSpeed() {
    return cFrontRightWheelSpeed;
}

int Motion::getSteeringActSpeed() {
    return cSteeringActSpeed;
}

int Motion::getBucketActSpeed() {
    return cBucketActSpeed;
}

int Motion::getBucketMotorSpeed() {
    return cBucketMotorSpeed;
}

int Motion::getConveryerMotorSpeed() {
    return cConveryerMotorSpeed;
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

    // Stop it!!!!!!!!!
    cDriveWheelsWrite(1470);
    cMoveSteeringWrite(1480);
    cMoveBucketsWrite(1470);
    cDriveBucketWrite(1480);
    cDriveConveyerWrite(1480);
}
  
// Ron: Function used to destroy the object (destructor)
Motion::~Motion() {}
