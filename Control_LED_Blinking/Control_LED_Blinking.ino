/**
 *  Control_LED_Blinking
 *
 *  Controls how many times per second an LED flashes. Flashes
 *  one time a second by default. The LED is controlled by serial
 *  in and reports back via serial out when the blinkRate is
 *  updated.
 *  
 *  To view the Serial Monitor:
 *  Control + Shift + M or Tools > Serial Monitor
 *  
 *  Created 18 October 2015
 *  Logan Rickert
 */

// Defines the ASCII 0 offset.
#define ASCII_0_OFFSET 48

// The pin the LED is connected too.
const int LED_PIN = 13;

// How fast the LED blinks per minute.
int blinkRate = 1;

/**
 *  This is the first method to run. Runs only once, at the
 *  start of the program.
 
 *  Sets LED_PIN's mode to OUTPUT.
 */
void setup() {
  // Initializes digital pin LED_PIN as an output.
  pinMode(LED_PIN, OUTPUT);

  // Sets up the Serial libray at 9600 bps (bits per second).
  Serial.begin(9600);
}

/**
 *  This method is called directly after setup() and 
 *  is called forever as soon as it finishes.
 
 *  Causes the LED on LED_PIN to blink 1 / blinkRate per second.
 */
void loop() {
  // Checks if any new serial data has come through.
  // If so, change @blinkRate.
  updateBlinkRate(blinkRate);
  
  // Makes the LED flash for 1 blinkRate of a second.
  blink(LED_PIN, 1000.0/blinkRate);
}

/**
 *  Changes the blinkRate value that is passed in if
 *  a new value has been read in from serial. Value is
 *  clamped to [0-9].
 
 *  @blinkRate - The value to change if a new number has been
 *  passed in through serial.
 */
void updateBlinkRate(int &blinkRate) {
  // Check to see if there is a new number at serial we haven't
  // read in yet.
  if (Serial.available() > 0) {
    
    // Get number from serial and ensure number is between 0
    // and 9.
    int delta = clamp0to9(getNumberFromSerial());

    Serial.print("Changing LED speed by: ");
    Serial.println(delta);
    
    blinkRate += delta;
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
int clamp0to9(int number) {
  if (number > 9) number = 9;
  if (number < 0) number = 0;
  return number;
}

/**
 *  blink asserts @pin high for half of @assertTime,
 *  then asserts @pin low for the second half of @assertTime.
 
 *  @pin - The pin to assert high for assertTime / 2,
 *  then assert low for assertTime / 2.
 *  @assertTime - How long the LED should be asserted for,
 *  measured in seconds.
 */
void blink(int pin, float assertTime) {
  digitalWrite(pin, HIGH);
  delay(assertTime / 2.0);
  digitalWrite(pin, LOW);
  delay(assertTime / 2.0);
}

