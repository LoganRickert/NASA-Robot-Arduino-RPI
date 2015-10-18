/**
 *  Control_Motor_Simple
 *
 *  A simple project that controls the speed of a motor
 *  attached to a RoboClaw through serial input.
 *  
 *  Serial Encoding:
 *  9 - increase 25
 *  8 - increase 20
 *  ...
 *  4 - increase 0
 *  3 - increase -5
 *  ...
 *  0 - increase -20
 *  
 *  To view the Serial Monitor:
 *  Control + Shift + M or Tools > Serial Monitor
 *  
 *  Created 18 October 2015
 *  Logan Rickert
 */

#include <Servo.h>

// Defines constants for motor pulse.
const int FULL_REVERSE = 1250;
const int STOP = 1500;
const int FULL_FORWARD = 1750;
const int SERVO_RANGE = FULL_FORWARD - STOP;

// Defines the ASCII 0 offset.
const int ASCII_0_OFFSET = 48;

// Attaches an RC signal on this pin that controls servoA.
const int SERVO_A_PIN = 6;

// Creates a new Servo object to control RoboClaw A.
Servo servoA;

// How fast servo A is moving.
int servoASpeed;

// Check to see if we've updated the speed. If we have,
// write the new value to servoA.
int lastServoASpeed;

/**
 *  This is the first method to run. Runs only once, at the
 *  start of the program.
 
 *  Attaches the servo motors and sets intial speed to stop.
 */
void setup() {
  // Attaches the RC signal on pin SERVO_A_PIN to the servo object 
  servoA.attach(SERVO_A_PIN);

  // Sets up the Serial libray at 9600 bps (bits per second).
  Serial.begin(9600);

  // Start servo A at speed 0.
  servoASpeed = STOP;

  lastServoASpeed = servoASpeed;
}

/**
 *  This method is called directly after setup() and 
 *  is called forever as soon as it finishes.
 
 *  Sets the speed of the motor.
 */
void loop() {
  // Checks if any new serial data has come through.
  // If so, change @servoASpeed.
  // Args: &rate, offset, modifier
  updateRate(servoASpeed, -4, 5);

  // Checks to see if the speed has changed.
  // If it has, update the servo's speed.
  if (servoASpeed != lastServoASpeed) {
    // Writes the new speed to the RoboClaw's A motor.
    servoA.writeMicroseconds(servoASpeed);

    lastServoASpeed = servoASpeed;
  }
}

/**
 *  Changes the @rate value that is passed in if
 *  a new value has been read in from serial. Value is
 *  clamped to [0-9].
 
 *  @rate - The value to change if a new number has been
 *  passed in through serial.
 *  @offset - Offsets the number added to rate
 *  @modifier - Multipies the delta * offset
 */
void updateRate(int &rate, int offset, int modifier) {
  // Check to see if there is a new number at serial we haven't
  // read in yet.
  if (Serial.available() > 0) {
    
    // Get number from serial and ensure number is between 0
    // and 9.
    int delta = clamp(getNumberFromSerial(), FULL_REVERSE, FULL_FORWARD);

    rate += ((delta + offset) * modifier);
  
    Serial.print("Changing speed to: ");
    Serial.println(rate);
  }
}

/**
 *  Returns the number passed in through serial minus the 
 *  ASCII offset for 0.
 */
int getNumberFromSerial() {
  return (Serial.read() - ASCII_0_OFFSET);
}

/**
 *  If the number is greater than 9 or less than 0, the
 *  number is clamped to 9 or 0 and returned.
 
 *  @number - The number to be clamped and returned.
 */
int clamp(int number, int high, int low) {
  if (number > high) number = high;
  if (number < low) number = low;
  return number;
}

