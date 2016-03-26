
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
int aBackLeftWheelEncoderPin = A0;
int aBackRightWheelEncoderPin = A0;
int aFrontLeftWheelEncoderPin = A0;
int aFrontRightWheelEncoderPin = A0;
int aSteeringActSensorPin = A0;
int aBucketActSensorPin = A0;
int aIRBackPin = A0;

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
  // Check if we have gotten
  // a new command. If so,
  // process it.
  functionB();

  sendUpdateData();

  delay(500);
}

void sendUpdateData() {
  Serial.print(sensor.getBackLeftWheelEncoder());
  Serial.print('-');
  Serial.print(sensor.getBackRightWheelEncoder());
  Serial.print('-');
  Serial.print(sensor.getFrontLeftWheelEncoder());
  Serial.print('-');
  Serial.print(sensor.getFrontRightWheelEncoder());
  Serial.print('-');
  Serial.print(sensor.getSteeringActSensor());
  Serial.print('-');
  Serial.print(sensor.getBucketActSensor());
  Serial.print('-');
  Serial.println(sensor.getIRBack());
}

// If command == 0, the last command
// has been processed
char commandType;

// The argument to the command
int arg;

// If ready, command is ready
// to be processed.
bool readyForNewCommand;

// A = motors
// arg = set speed
// B = motor left front
// arg = set left front speed

/**
 * @breif
 */
void functionA() {
  while (!readyForNewCommand && Serial.available() > 0) {
    // Make sure the last command
    // is processed before we
    // start anew and overwritting it.
    if (readyForNewCommand == false) {
      if (commandType == 0) {
        // get the command
        commandType = Serial.read();
      } else {
        // get next character
        char character = Serial.read();

        // If character is \n, it's the
        // end of the current command.
        if (character == '\n') {
          readyForNewCommand = true;
          Serial.print(commandType);
          Serial.print('-');
          Serial.println(arg);
        } else {
          // Shift arg by 1 to make room
          // for the new number.
          arg *= 10;
          arg += (character - '0');
        }
      }
    }
  }
}

// This runs at the start of the
// main loop.
void functionB() {

  while (Serial.available() > 0) {
    // Update input from serial.
    functionA();

    if (readyForNewCommand == true) {
      doStuff(commandType, arg);
      readyForNewCommand = false;
      commandType = 0;
      arg = 0;
    }
  }
}

void doStuff(char command, int arg) {
  switch (command) {
    case 'A':
      motion.cDriveWheelsWrite(arg);
      break;
    case 'B':
      motion.cDriveBLWWrite(arg);
      break;
    case 'C':
      motion.cDriveBRWWrite(arg);
      break;
    case 'D':
      motion.cDriveFLWWrite(arg);
      break;
    case 'E':
      motion.cDriveFRWWrite(arg);
      break;
    case 'F':
      motion.cDriveBucketWrite(arg);
      break;
    case 'G':
      motion.cDriveConveyerWrite(arg);
      break;
    case 'H':
      motion.cMoveSteeringWrite(arg);
      break;
    case 'I':
      motion.cMoveBucketsWrite(arg);
      break;
    case 'J':
      Serial.print('J');
      Serial.println(sensor.getBackLeftWheelEncoder());
      break;
    case 'K':
      Serial.print('K');
      Serial.println(sensor.getBackRightWheelEncoder());
      break;
    case 'L':
      Serial.print('L');
      Serial.println(sensor.getFrontLeftWheelEncoder());
      break;
    case 'M':
      Serial.print('M');
      Serial.println(sensor.getFrontRightWheelEncoder());
      break;
    case 'N':
      Serial.print('N');
      Serial.println(sensor.getSteeringActSensor());
      break;
    case 'O':
      Serial.print('O');
      Serial.println(sensor.getBucketActSensor());
      break;
    case 'P':
      Serial.print('P');
      Serial.println(sensor.getIRBack());
      break;
  }
}