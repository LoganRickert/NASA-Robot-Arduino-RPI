import serial
import time

# Connect to the Arduino.
connection = serial.Serial('/dev/ttyACM0', 9600)

# Wait for the Arduino to restart
# The Arduino restarts with every new Serial
#   connection.
print("Please wait for device to restart...");
time.sleep(2)
print("Connected!")

# To exit the program, Control + C
while True:
  # Ask the user what they want to change the
  # value by
  delta = raw_input("Value to change by: ")

  # Write to the Arduino the value to change.
  connection.write(delta)

  # Print out the response from the Arduino
  print connection.readline()
