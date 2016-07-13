
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
    int tempa = analogRead(cSteeringActSensor) / 5;
    int temp = tempa - cSteeringActSensorLast;
    if (temp < 0) temp *= -1;
    if (temp > 5) return cSteeringActSensorLast;
    else {
      cSteeringActSensorLast = tempa;
      return tempa; 
    }
}

// Ron: Function used to get the bucket system angle
int Sensor::getBucketActSensor() {
    int tempa = analogRead(cBucketActSensor) / 5;
    int temp = tempa - cBucketActSensorLast;
    
    if (temp < 0) temp *= -1;
    if (temp > 5) return cBucketActSensorLast;
    else {
      cBucketActSensorLast = tempa;
      return tempa; 
    }
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
    
    int avga = 0;
    int avgb = 0;
    int totala = 0;
    int totalb = 0;
    delay(100);
    for (int i = 0; i < 50; i++) {totala += 1; int num = analogRead(cBucketActSensor) / 5; Serial.println(num); avga += num; delay(10); }
    for (int i = 0; i < 50; i++) {totalb += 1; avgb += analogRead(cSteeringActSensor) / 5; delay(10);}
    delay(10);
    cSteeringActSensorLast = avgb / totala;
    delay(10);
    cBucketActSensorLast = avga / totalb;
    
    Serial.println(cSteeringActSensorLast);
    Serial.println(cBucketActSensorLast);
}

// Ron: Function used to destroy the object (destructor)
Sensor::~Sensor() {}
