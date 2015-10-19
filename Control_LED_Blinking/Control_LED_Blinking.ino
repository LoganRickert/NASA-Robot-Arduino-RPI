/**
 *  Control_LED_Blinking
 *
 *  Controls how many times per second an LED flashes. Flashes
 *  10 time a second by default. The LED is controlled by serial
 *  in and reports back via serial out when the blinkRate is
 *  updated. The value of light must blink at least 1 time a second.
 *  
 *  Serial Encoding:
 *  9 - increase 9
 *  8 - increase 8
 *  ...
 *  4 - increase 4
 *  3 - increase 3
 *  ...
 *  0 - Flashes 1 time a second
 *  
 *  To view the Serial Monitor:
 *  Control + Shift + M or Tools > Serial Monitor
 *  
 *  Created 18 October 2015
 *  Logan Rickert
 */

// Defines the ASCII 0 offset.
const int ASCII_0_OFFSET = 48;

// Tells the program if a new line has come in on serial
int newLine;

// Tells the program what the entire number that came in on serial was.
int lineNumber;

// The pin the LED is connected too.
const int LED_PIN = 13;

// How fast the LED blinks per minute.
int blinkRate = 10;

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

  // There are no new complete numbers from serial yet.
  newLine = 0;
  lineNumber = 0;
}

/**
 *  This method is called directly after setup() and 
 *  is called forever as soon as it finishes.
 
 *  Causes the LED on LED_PIN to blink 1 / blinkRate per second.
 */
void loop() {
  // Checks if any new serial data has come through.
  // If so, change @blinkRate.
  // Args: &rate, offset, modifier
  updateRate(blinkRate, 0, 1);
  
  // Makes the LED flash for 1 blinkRate of a second.
  blink(LED_PIN, 1000.0 / blinkRate);
}

/**
 *  Changes the @rate value that is passed in if
 *  a new value has been read in from serial. Value is
 *  clamped to [0-9]. The value of @rate will never go
 *  below 1.
 
 *  @rate - The value to change if a new number has been
 *  passed in through serial.
 *  @offset - Offsets the number added to rate
 *  @modifier - Multipies the delta * offset
 */
void updateRate(int &rate, int offset, int modifier) {
  // Check to see if there is a new number at serial we haven't
  // read in yet.
  if (Serial.available() > 0) {
    getLineNumberFromSerial();
  }

  // Check if a new number from serial has been read in.
  if (newLine) {
    // Get number from serial and ensure number is between 1
    // and 21. (1 and 21 are arbitrary. Based on [-1 to 1] range of
    // controller axis input.
    int delta = clamp(lineNumber, 1, 21);

    rate = ((delta + offset) * modifier);
  
    Serial.print("Changing speed by ");
    Serial.print(((delta + offset) * modifier));
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

