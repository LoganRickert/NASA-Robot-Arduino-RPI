#ifndef SENSOR_H
#define SENSOR_H

#include <Arduino.h>

class Sensor {

	public:
		Sensor(int, int, int, int, int, int, int);
		~Sensor();
		
        //Ron: Function used to get the encoder value
        int backLeftWheelEncoderGet();

        //Ron: Function used to get the encoder value
        int backRightWheelEncoderGet();

        //Ron: Function used to get the encoder value
        int frontLeftWheelEncoderGet();

        //Ron: Function used to get the encoder value
        int frontRightWheelEncoderGet();

        //Ron: Function used to get the stearing angle
        int steeringActSensorGet();

        //Ron: Function used to get the bucket system angle
        int bucketActSensorGet();

        //Ron: Function used to get the robot distance from object in back
        int IRGet();

	private:
  		// Ron: Class Properties

        // Ron: Encoder Pins
        int cBackLeftWheelEncoder;
        int cBackRightWheelEncoder;
        int cFrontLeftWheelEncoder;
        int cFrontRightWheelEncoder;
        int cSteeringActSensor;
        int cBucketActSensor;
        int cIRBack;
};

#endif
