
// Ron: Class will be used to read the sensors (sensor objects)

#include "Sensor.h"

// Ron: Function used to get the encoder value
int Sensor::getBackLeftWheelEncoder() {
    return analogRead(cBackLeftWheelEncoder);
}

// Ron: Function used to get the encoder value
int Sensor::getBackRightWheelEncoder() {
    return analogRead(cBackRightWheelEncoder);
}

// Ron: Function used to get the encoder value
int Sensor::getFrontLeftWheelEncoder() {
    return analogRead(cFrontLeftWheelEncoder);
}

// Ron: Function used to get the encoder value
int Sensor::getFrontRightWheelEncoder() {
    return analogRead(cFrontRightWheelEncoder);
}

// Ron: Function used to get the stearing angle
int Sensor::getSteeringActSensor() {
    return analogRead(cSteeringActSensor);
}

// Ron: Function used to get the bucket system angle
int Sensor::getBucketActSensor() {
    return analogRead(cBucketActSensor);
}

// Ron: Function used to get the robot distance from object in back
int Sensor::getIRBack() {
    return analogRead(cIRBack);
}

// Ron: Function used to create the object (constructor)
Sensor::Sensor(int aPin1,int aPin2, int aPin3, int aPin4, int aPin5, int aPin6, int aPin7) { 
    cBackLeftWheelEncoder = aPin1;
    cBackRightWheelEncoder = aPin2;
    cFrontLeftWheelEncoder = aPin3;
    cFrontRightWheelEncoder = aPin4;
    cSteeringActSensor = aPin5;
    cBucketActSensor = aPin6;
    cIRBack = aPin7;
}

// Ron: Function used to destroy the object (destructor)
Sensor::~Sensor() {}
