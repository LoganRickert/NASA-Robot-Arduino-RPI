#ifndef SENSOR_H
#define SENSOR_H

#include <Arduino.h>

class Sensor {

	public:
		Sensor(int, int, int, int, int, int, int);
		~Sensor();
		
        //Ron: Function used to get the encoder value
        int getBackLeftWheelEncoder();

        //Ron: Function used to get the encoder value
        int getBackRightWheelEncoder();

        //Ron: Function used to get the encoder value
        int getFrontLeftWheelEncoder();

        //Ron: Function used to get the encoder value
        int getFrontRightWheelEncoder();

        //Ron: Function used to get the stearing angle
        int getSteeringActSensor();

        //Ron: Function used to get the bucket system angle
        int getBucketActSensor();

        //Ron: Function used to get the robot distance from object in back
        int getIRBack();

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
