
#include <Servo.h>
#include "Motion.h"
#include "Sensor.h"

/*
=============================================================================
Title:    Arduino classes utility file
Authors:  Ron Picard, Logan Rickert
Purpose:  Used to create Motion objects to send commands to the robot, and to
          create Sensor objects to get sensor values from the sensors
Created:  01/30/16
Modified: 03/20/16
=============================================================================
Use case: just an in import file to create these objects
============================================================================
*/ 

// Motion Pins
int gBackLeftWheelPin = 0;
int gBackRightWheelPin = 0;
int gFrontLeftWheelPin = 0;
int gFrontRightWheelPin = 0;
int gSteeringActPin = 0;
int gBucketActPin = 0;
int gBucketMotorPin = 0;
int gConveryerMotorPin = 0;

// Senosr Pins
int aBackLeftWheelEncoderPin = 0;
int aBackRightWheelEncoderPin = 0;
int aFrontLeftWheelEncoderPin = 0;
int aFrontRightWheelEncoderPin = 0;
int aSteeringActSensorPin = 0;
int aBucketActSensorPin = 0;
int aIRBackPin = 0;

Motion motion(
  gBackLeftWheelPin,
  gBackRightWheelPin,
  gFrontLeftWheelPin,
  gFrontRightWheelPin,
  gSteeringActPin,
  gBucketActPin,
  gBucketMotorPin,
  gConveryerMotorPin
);

Sensor sensor(
  aBackLeftWheelEncoderPin,
  aBackRightWheelEncoderPin,
  aFrontLeftWheelEncoderPin,
  aFrontRightWheelEncoderPin,
  aSteeringActSensorPin,
  aBucketActSensorPin,
  aIRBackPin
);

void setup() {
  // Begin serial connections
  Serial.begin(9600);

  // Create motion object

  // Create sensor object
}

void loop() {
  // read serial valuesm parse this for values
  //int num = Serial.read();

//  passMotion(lfor,num);

  // write sensor values
//  Serial.write();
}
