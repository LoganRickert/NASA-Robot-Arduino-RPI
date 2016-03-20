
#ifndef MOTION_H
#define MOTION_H

#include <Servo.h>
#include <Arduino.h>

class Motion {

	public:
		Motion(int,int, int, int, int, int, int, int);
		~Motion();

		// DC Motors
		// To do: control one wheel at a time.
		// To do: add gets for current write speed
		// of each motor.
		void cDriveWheelsWrite(int, int, int, int);
		void cDriveWheelsWrite(int);
		void cDriveBLWWrite(int);
		void cDriveBRWWrite(int);
		void cDriveFLWWrite(int);
		void cDriveFRWWrite(int);
		void cDriveBucketWrite(int);
		void cDriveConveyerWrite(int);

		// Actuators
		void cMoveSteeringWrite(int);
		void cMoveBucketsWrite(int);

		// Gets
		int getConveryerMotorSpeed();
		int getBucketMotorSpeed() ;
		int getBucketActSpeed();
		int getSteeringActSpeed();
		int getFrontRightWheelSpeed();
		int getFrontLeftWheelSpeed();
		int getBackRightWheelSpeed();
		int getBackLeftWheelSpeed();

	private: 
		// Ron: Class Properties

		// Ron: The properties are Servo objects
		Servo cBackLeftWheel;
		Servo cBackRightWheel;
		Servo cFrontLeftWheel;
		Servo cFrontRightWheel;
		Servo cBucketMotor;
		Servo cConveryerMotor;
		Servo cSteeringAct;
		Servo cBucketAct;

		int cBackLeftWheelSpeed;
		int cBackRightWheelSpeed;
		int cFrontLeftWheelSpeed;
		int cFrontRightWheelSpeed;
		int cSteeringActSpeed;
		int cBucketActSpeed;
		int cBucketMotorSpeed;
		int cConveryerMotorSpeed;
};

#endif
