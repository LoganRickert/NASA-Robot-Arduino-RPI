

#ifndef MOTION_H
#define MOTION_H

#include <Servo.h>
#include <Arduino.h>

class Motion {

	public:
		Motion(int,int, int, int, int, int, int, int);
		~Motion();

		// DC Motors
		void cDriveWheelsWrite(int, int, int, int);
		void cDriveBucketWrite(int);
		void cDriveConveyerWrite(int);

		// Actuators
		void cMoveSteeringWrite(int);
		void cMoveBucketsWrite(int);

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
};

#endif
