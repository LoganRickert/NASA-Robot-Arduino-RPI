/**
 *  Control_Motor_Simple
 *
 *  A simple project that controls the speed of a motor
 *  attached to a RoboClaw through serial input.
 *  
 *  Serial Encoding:
 *  21 - 100% forward
 *  16 - 50% forward
 *  11 - 0% stop
 *   6 - 50% reverse
 *   1 - 100% reverse
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

// How fast servo A is moving, based on percentage.
// 0 - 49% = Reverse
// 50% = Stop
// 51 - 100% = Foward
float servoAPercent;

// Check to see if we've updated the speed. If we have,
// write the new value to servoA.
float lastServoAPercent;

// Tells the program if a new line has come in on serial
int newLine;

// Tells the program what the entire number that came in on serial was.
int lineNumber;

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

  // There are no new complete numbers from serial yet.
  newLine = 0;
  lineNumber = 0;

  // Start servo A at speed 50.
  servoAPercent = .50;

  lastServoAPercent = servoAPercent;
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
  updateRate(servoAPercent, 0, 1);

  // Checks to see if the speed has changed.
  // If it has, update the servo's speed.
  if (servoAPercent != lastServoAPercent) {
    // Writes the new speed to the RoboClaw's A motor.
    servoA.writeMicroseconds(STOP + (SERVO_RANGE * servoAPercent));

    lastServoAPercent = servoAPercent;
  }
}

/**
 *  Changes the @rate value that is passed in if
 *  a new value has been read in from serial. Value is
 *  clamped to [1-21].
 
 *  @rate - The value to change if a new number has been
 *  passed in through serial.
 *  @offset - Offsets the number added to rate
 *  @modifier - Multipies the delta * offset
 */
void updateRate(float &rate, int offset, int modifier) {
  // Check to see if there is a new number at serial we haven't
  // read in yet.
  if (Serial.available() > 0) {
    getLineNumberFromSerial();
  }

  // Check if a new number from serial has been read in.
  if (newLine) {
    // Get number from serial and ensure number is between 1
    // and 21.
    int delta = clamp(lineNumber, 1, 21);

    Serial.print(rate);

    // Get the percentage with 11 being 0%.
    // Will be between -100% and 100%.
    rate = ((delta - 11) / 10.0);
    
    Serial.print(" to ");
    Serial.println(rate);

    // Reset the values.
    newLine = 0;
    lineNumber = 0;
  }
}

/**
 *  Gets the entire number passed in through serial, ending in a newline.
 *  Sets newLine equal to 1 once the entire number has been read in.
 *  The entire number is stored in lineNumber.
 */
void getLineNumberFromSerial() {
  if (Serial.available() > 0) {
    char character = Serial.read();

    // If we have reached the end of the line.
    if (character == '\n') {
      Serial.println(character);
      newLine = 1;
    } else {
      // Make room for new number
      lineNumber *= 10;
      // Add number to end of lineNumber.
      lineNumber += (character - ASCII_0_OFFSET);
    }
  }
}

/**
 *  If the number is greater than HIGH or less than LOW, the
 *  number is clamped to HIGH or LOW and returned.
 
 *  @number - The number to be clamped and returned.
 *  @high - The upper limit of the number.
 *  @low - The lower limit of the number.
 */
int clamp(int number, int low, int high) {
  if (number > high) number = high;
  if (number < low) number = low;
  return number;
}

