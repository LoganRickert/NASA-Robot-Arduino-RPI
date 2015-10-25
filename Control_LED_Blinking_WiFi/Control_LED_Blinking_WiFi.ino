/**
 *  Control_LED_Blinking
 *
 *  Controls how many times per second an LED flashes. Flashes
 *  10 time a second by default. The LED is controlled by serial
 *  in and reports back via serial out when the blinkRate is
 *  updated. The value of light must blink at least 1 time a second.
 *  
 *  Serial Encoding:
 *  21 - MAX, 21 times a second
 *  9 - increase to 9
 *  8 - increase to 8
 *  ...
 *  4 - increase to 4
 *  3 - increase to 3
 *  ...
 *  1 - Flashes 1 time a second
 *  
 *  To view the Serial Monitor:
 *  Control + Shift + M or Tools > Serial Monitor
 *  
 *  Created 18 October 2015
 *  Logan Rickert
 */

#include <SPI.h>
#include <WiFi.h>

// Defines the ASCII 0 offset.
const int ASCII_0_OFFSET = 48;

const int ON = 1;
const int OFF = 0;

// Tells the program if a new line has come in on serial
int newLine;

// Tells the program what the entire number that came in on serial was.
int lineNumber;

// The pin the LED is connected too.
const int LED_PIN = 8;
const int LED_PIN_2 = 6;

// How fast the LED blinks per minute.
int blinkRate;

// How many miliseconds have we waited since last blink.
// We can't just wait(blinkRate) because we have to check
// the serial every milisecond for new input to remove
// extreme latency.
int currentBlinkDelayCount;

// If the LED should be on or off.
int switchPos;

// Name of the WiFi
char ssid[] = "BoffinCisco";

// WiFi password
char ssidPassword[] = "boffin111";

// status of the WiFi shield
int wifiSheildStatus = WL_IDLE_STATUS;

// IP of the server
IPAddress server(192, 168, 1, 108);

WiFiClient client;

/**
 *  This is the first method to run. Runs only once, at the
 *  start of the program.
 
 *  Sets LED_PIN's mode to OUTPUT.
 */
void setup() {
  // Initializes digital pin LED_PIN as an output.
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);

  blinkRate = 10;
  currentBlinkDelayCount = 0;
  switchPos = ON;

  // Sets up the Serial libray at 9600 bps (bits per second).
  Serial.begin(9600);

  // There are no new complete numbers from serial yet.
  newLine = 0;
  lineNumber = 0;

  setupWiFi();
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
  switchPos = updateLED(LED_PIN, LED_PIN_2, 1000.0 / blinkRate, switchPos);

  // Hold updateLED by 1 milisecond.
  delay(1);
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
  if (client.available()) {
    getLineNumberFromSerial();
  }

  // Check if a new number from serial has been read in.
  if (newLine) {
    // Get number from serial and ensure number is between 1
    // and 21. (1 and 21 are arbitrary. Based on [-1 to 1] range of
    // controller axis input.
    int delta = clamp(lineNumber, 1, 21);

    Serial.print(rate);
    
    rate = ((delta + offset) * modifier);
    
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
  if (client.available()) {
    char character = client.read();

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

void setupWiFi() {
  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present. Quitting."); 
    // don't continue:
    while(true);
  }

  // attempt to connect to Wifi network:
  while (wifiSheildStatus != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    wifiSheildStatus = WiFi.begin(ssid, ssidPassword);
    
    // wait 10 seconds for connection:
    delay(10000);
  }
  
  Serial.println("Connected to wifi");
  printWifiStatus();

  // if you get a connection, report back via serial:
  if (client.connect(server, 1338)) {
    Serial.println("connected to server");
  } else {
    Serial.println("Not connected!");
  }
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

/**
 *  blink asserts @pin high for half of @assertTime,
 *  then asserts @pin low for the second half of @assertTime.
 
 *  @pin - The pin to assert high for assertTime / 2,
 *  then assert low for assertTime / 2.
 *  @assertTime - How long the LED should be asserted for,
 *  measured in seconds.
 *  @switchState - If the LED should be on or off.
 *  @return - The new state of the switch.
 */
int updateLED(int pin, int pin2, float assertTime, int switchState) {
  // If we have held ON or OFF half of the total assert time, switch.
  if (currentBlinkDelayCount > assertTime / 2.0) {
    switchState = (switchState + 1) % 2;
    currentBlinkDelayCount = 0;
    if (switchState == ON) {
      digitalWrite(pin, HIGH);
      digitalWrite(pin2, LOW);
    } else {
      digitalWrite(pin, LOW);
      digitalWrite(pin2, HIGH);
    }
  } else {
    currentBlinkDelayCount++;
  }

  return switchState;
}

