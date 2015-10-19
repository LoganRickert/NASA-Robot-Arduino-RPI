import pygame
import serial
from pygame.locals import *


#########

## Ignore all the pygame stuff.
## It's just here to get input from controller easily.

#########


# The width of the pygame window
WIN_WIDTH = 640
WIN_HEIGHT = 480

# Connect to the Arduino.
arduino = serial.Serial('/dev/ttyACM0', 9600)

def main():
  # Ignore all this stuff
  pygame.init()
  screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

  pygame.display.set_caption("Joystick test")
  game_clock = pygame.time.Clock()

  joysticks = []

  for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

    print "Adding joystick", joysticks[-1].get_name()
  
  while True:
    pygame.time.wait(500)
    print "Starting new cycle"
    hasJoyUpdated = False    

    for event in pygame.event.get():
      if event.type == QUIT:
        print "Exiting the window..."
        exit(0)
      elif event.type == KEYDOWN:
        print "Key down:", event.key
      elif event.type == JOYAXISMOTION:
        # 1 = Left stick, up to down, -1 to 1
        # 2 = Left stick, left to right, -1 to 1
        # 3 = Right stick, left to right, -1 to 1
        # 4 = Right stick, up to down, -1 to 1
        if event.axis == 1 and not hasJoyUpdated:
          hasJoyUpdated = True
          print "joystick", joysticks[event.joy].get_name()
          
          # Invert axis, change range from -1 to 1 to -10 to 10
          # Also change from float to int to a string.
          value = str(int(event.value * 10) * -1)
          print "axis", event.axis, "value", value
          
          # Send it to the Arduino
          arduino.write(value)
          print arduino.readline()

if __name__ == "__main__":
  main()
