/**
 *  Control_Motor_Simple
 *
 *  A simple project that controls the speed of a motor
 *  attached to a RoboClaw through serial input.
 *  
 *  Mode 2 Setting 3
 *  
 *  Serial Encoding:
 *  40 - 100% forward
 *  30 - 50% forward
 *  20 - 0% stop
 *  10 - 50% reverse
 *   0 - 100% reverse
 *  
 *  To view the Serial Monitor:
 *  Control + Shift + M or Tools > Serial Monitor
 *  
 *  Created 18 October 2015
 *  Logan Rickert
 */

#include <Servo.h>
#include <SPI.h>
#include <WiFi.h>

// Defines constants for motor pulse.
const int FULL_REVERSE = 1250;
const int STOP = 1500;
const int FULL_FORWARD = 1750;
const int SERVO_RANGE = FULL_FORWARD - STOP;

// Defines the ASCII 0 offset.
const int ASCII_0_OFFSET = '0';

// Defines the ASCII A offset.
// We want 'A' to == 1.
const int ASCII_A_OFFSET = 'A' - 1;

// Attaches an RC signal on this pin that controls servoA.
const int SERVO_A_PIN = 48;
const int SERVO_B_PIN = 44;
const int SERVO_C_PIN = 40;
const int SERVO_D_PIN = 36;
const int LINEAR_A_PIN = 47;

const int LED_PIN = 24;
const int LED_PIN_2 = 25;
const int LED_PIN_3 = 22;
const int LED_PIN_4 = 23;

const int LIGHT_RIGHT = A14;
const int LIGHT_MIDDLE = A13;
const int LIGHT_LEFT = A12;

// Creates a new Servo object to control RoboClaw A.
Servo servoA;
Servo servoB;
Servo servoC;
Servo servoD;
Servo linearA;

// How fast servo A is moving, based on percentage.
// 0 - 49% = Reverse
// 50% = Stop
// 51 - 100% = Foward
float servoAPercent;
float actuatorPercent;

// Check to see if we've updated the speed. If we have,
// write the new value to servoA.
float lastServoAPercent;
float lastActuatorPercent;

int servoActive;
int steeringActive;

// Tells the program if a new line has come in on serial
int newLine;

// Tells the program what the entire number that came in on serial was.
int lineNumber;

// What we should do with lineNumber.
// 1 - Forward / Backwards
// 2 - Left / Right
int command;
int readCommand;

char ssid[] = "NASA_Robot";
char ssid_password[] = "DoctorThomas";

int status = WL_IDLE_STATUS;

IPAddress server(192, 168, 1, 113);

WiFiClient client;

const int buttonPin = 19;     // the number of the pushbutton pin
int state;
int buttonCount;

int nowState = 0;

/**
 *  This is the first method to run. Runs only once, at the
 *  start of the program.
 
 *  Attaches the servo motors and sets intial speed to stop.
 */
void setup() {
  // Attaches the RC signal on pin SERVO_A_PIN to the servo object 
  servoA.attach(SERVO_A_PIN);
  servoB.attach(SERVO_B_PIN);
  servoC.attach(SERVO_C_PIN);
  servoD.attach(SERVO_D_PIN);
  linearA.attach(LINEAR_A_PIN);

  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);
  pinMode(LED_PIN_3, OUTPUT);
  pinMode(LED_PIN_4, OUTPUT);
  
  pinMode(buttonPin, INPUT);
  state = 1;
  
  digitalWrite(LED_PIN, LOW);
  digitalWrite(LED_PIN_2, LOW);
  digitalWrite(LED_PIN_3, LOW);
  digitalWrite(LED_PIN_4, LOW);

  // Sets up the Serial libray at 9600 bps (bits per second).
  Serial.begin(9600);

  // There are no new complete numbers from serial yet.
  newLine = 0;
  lineNumber = 0;
  readCommand = 0;
  command = 0;
  
  servoActive = 0;
  steeringActive = 0;

  // Start servo A at speed 50.
  servoAPercent = .50;
  actuatorPercent = .50;

  lastServoAPercent = servoAPercent;
  lastActuatorPercent = actuatorPercent;
  
  servoA.writeMicroseconds(STOP - 50);
  servoB.writeMicroseconds(STOP - 50);
  servoC.writeMicroseconds(STOP - 50);
  servoD.writeMicroseconds(STOP - 50);
  linearA.writeMicroseconds(STOP - 42);

  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present. Writing out."); 
    // Don't continue:
    digitalWrite(LED_PIN, HIGH);
    while(true);
  }

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, ssid_password);

    // Wait 10 seconds for connection:
    blinkLED(LED_PIN, 10);
  }
  Serial.println("Connected to wifi");
  printWifiStatus();

  connectToServer();
}

void blinkLED(int led, int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(led, HIGH);
    delay(500);
    digitalWrite(led, LOW);
    delay(500);
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
 *  This method is called directly after setup() and 
 *  is called forever as soon as it finishes.
 
 *  Sets the speed of the motor.
 */
void loop() {
  updateButtonState();
  
  if (!state) {
    updateSensorStatus(servoAPercent, actuatorPercent);
  } else {
    // Checks if any new serial data has come through.
    // If so, change @servoASpeed.
    // Args: &rate, offset, modifier
    updateRate(servoAPercent, 0, 1);
  }

  // Checks to see if the speed has changed.
  // If it has, update the servo's speed.
  if (servoAPercent != lastServoAPercent) {
    Serial.println(command);
    if (command == 1 || servoActive) {
      // Writes the new speed to the RoboClaw's A motor.
      servoA.writeMicroseconds(STOP - (SERVO_RANGE * -servoAPercent) - 50);
      servoB.writeMicroseconds(STOP - (SERVO_RANGE * -servoAPercent) - 50);
      servoC.writeMicroseconds(STOP + (SERVO_RANGE * -servoAPercent) - 50);
      servoD.writeMicroseconds(STOP + (SERVO_RANGE * -servoAPercent) - 50);
    } else if (command == 2) {
      linearA.writeMicroseconds(STOP - (SERVO_RANGE * -servoAPercent) - 41.5);
    }
    
    lastServoAPercent = servoAPercent;
    command = 0;
  }
  
  if (actuatorPercent != lastActuatorPercent) {
    linearA.writeMicroseconds(STOP - (SERVO_RANGE * -actuatorPercent) - 41.5);
    lastActuatorPercent = actuatorPercent;
  }

  delay(1);
}

void updateButtonState() {
  if (buttonCount > 2000) {
    int yeah = digitalRead(buttonPin);
    if (buttonCount % 5000 == 0) Serial.println(yeah);
    if (yeah) {
      Serial.println("State changed");
      state = (state + 1) % 2;
      
      servoActive = 0;
      steeringActive = 0;
      
      if (state && client.connected()) {
        client.println("10");
      }
      
      Serial.println(state);
      buttonCount = 0;
      servoA.writeMicroseconds(STOP - 50);
      servoB.writeMicroseconds(STOP - 50);
      servoC.writeMicroseconds(STOP - 50);
      servoD.writeMicroseconds(STOP - 50);
      linearA.writeMicroseconds(STOP - 41.5);
    }
  }

  if (!state) {
    digitalWrite(LED_PIN_4, HIGH);
  } else {
    digitalWrite(LED_PIN_4, LOW);
  }
  
  buttonCount++;
}

void updateSensorStatus(float &wheelRate, float &actuatorRate) {
  int right = clamp(analogRead(LIGHT_RIGHT) - 550, 0, 1);
  int middle = clamp(analogRead(LIGHT_MIDDLE) - 550, 0, 1);
  int left = clamp(analogRead(LIGHT_LEFT) - 550, 0, 1);
  
  servoActive = 0;
  steeringActive = 0;
  
  int deltaWheels = 20;
  int deltaAct = 20;
  
  if (left && !(middle && right)) {
    deltaWheels = 12;
    servoActive = 1;
    deltaAct = 0;
  } else if (right && !(middle && left)) {
    deltaWheels = 12;
    servoActive = 1;
    deltaAct = 20;
  } else if (middle || (left && right)) {
    deltaWheels = 12;
    servoActive = 1;
    deltaAct = 10;
  } else if (middle && left && !right) {
    deltaWheels = 12;
    servoActive = 1;
    deltaAct = 10;
  } else if (middle && right && !left) {
    deltaWheels = 12;
    servoActive = 1;
    deltaAct = 10;
  } else {
    deltaWheels = 10;
    servoActive = 1;
    deltaAct = 10;
  }
  
  if (!state && client.connected()) {
    int ishNowState = 0;
    if (!left && !middle && !right) {
      ishNowState = 10;
    } else {
      ishNowState = 20;
    }
  
    if (left) ishNowState += 1;
    if (right) ishNowState += 2;
    if (middle) ishNowState += 4;
    
    if (ishNowState != nowState) {
      client.println(ishNowState);
      client.flush();
      nowState = ishNowState;
    }
  }
  
  wheelRate = ((deltaWheels - 10) / 10.0);
  actuatorRate = ((deltaAct - 10) / 10.0);
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
  if (!client.connected()) {
     Serial.println("No longer connected! Stopping motors.");
     servoA.writeMicroseconds(STOP - 50);
     servoB.writeMicroseconds(STOP - 50);
     servoC.writeMicroseconds(STOP - 50);
     servoD.writeMicroseconds(STOP - 50);
     linearA.writeMicroseconds(STOP - 41.5);
     connectToServer();
  }
  // Check to see if there is a new number at serial we haven't
  // read in yet.
  if (client.available()) {
    getLineNumberFromSerial();
  }

  // Check if a new number from serial has been read in.
  if (newLine) {
    // Get number from serial and ensure number is between 1
    // and 21.
    int delta = clamp(lineNumber, 0, 20);

    Serial.print(command);
    Serial.print(" ");
    Serial.print(rate);

    // Get the percentage with 11 being 0%.
    // Will be between -100% and 100%.
    rate = ((delta - 10) / 10.0);
    command = readCommand;
    
    Serial.print(" to ");
    Serial.println(rate);

    // Reset the values.
    newLine = 0;
    lineNumber = 0;
    readCommand = 0;
  }
}

void connectToServer() {
  // if you get a connection, report back via serial:
  digitalWrite(LED_PIN_2, HIGH);
  digitalWrite(LED_PIN_3, LOW);
  while (!client.connect(server, 1338)) {
    Serial.println("Not connected!");
    // Wait 5 seconds
    blinkLED(LED_PIN_2, 5);
    digitalWrite(LED_PIN_2, HIGH);
  }
  
  client.println("arduino");
  
  digitalWrite(LED_PIN_2, LOW);
  digitalWrite(LED_PIN_3, HIGH); 
  
  Serial.println("Connected to server!");
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
      newLine = 1;
    } else {
      if (!readCommand) {
        readCommand = (character - ASCII_A_OFFSET);
      } else {
        // Make room for new number
        lineNumber *= 10;
        // Add number to end of lineNumber.
        lineNumber += (character - ASCII_0_OFFSET);
      }
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

