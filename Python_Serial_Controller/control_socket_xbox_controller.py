import pygame
import serial
from pygame.locals import *
import socket

#########

## Ignore all the pygame stuff.
## It's just here to get input from controller easily.

#########


# The width of the pygame window
WIN_WIDTH = 640
WIN_HEIGHT = 480

# Connect to the Arduino.
server_addr = ('', 1338)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
  print 'Starting server on %s:%s' % server_addr
  socket.bind(server_addr)
  socket.listen(5)

  print 'Waiting for client...'
  client, addr = socket.accept()
  
  print client, addr

  # Wait until the last serial write has finished
  serialWriteDone = True
  # What the new value to write is.
  serialOutputToWrite = 0
  # What the last value wrote was.
  lastSerialOutputToWrite = serialOutputToWrite

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
    pygame.time.wait(60)

    # - print "Checking", serialOutputToWrite, lastSerialOutputToWrite

    if serialWriteDone and serialOutputToWrite != lastSerialOutputToWrite:
      serialWriteDone = False
      client.send(serialOutputToWrite + '\n')

      #while arduino.inWaiting() > 0:
      #  print arduino.read(arduino.inWaiting())

      lastSerialOutputToWrite = serialOutputToWrite
      serialWriteDone = True

    # Get the current value of the joystick. Between 1 (down) and 1 (up)
    # -1 = Flip the axis
    # 10 = increase range from -1 to 1 to -10 to 10
    axis1Pos = joysticks[0].get_axis(1) * -1 * 10

    # Get how far the trigger is pulled
    triggerMult = joysticks[0].get_axis(5)
    # I'm honestly not sure what this does anymore. It works though.
    triggerNormal = (((triggerMult + 1.0) / 2.0) + 1.0) / 2.0

    # Value is between 5 and 15 when trigger is at -1
    # Value is between 0 and 20 when trigger is at  1
    valueFinal = str(int(round(((axis1Pos * triggerNormal) + 10))))
    print valueFinal

    serialOutputToWrite = valueFinal

    # Ignore this stuff
    for event in pygame.event.get():
      if event.type == QUIT:
        print "Exiting the window..."
        exit(0)
      elif event.type == KEYDOWN:
        print "Key down:", event.key
      elif event.type == JOYAXISMOTION:
        pass
        # 1 = Left stick, up to down, -1 to 1
        # 2 = Left stick, left to right, -1 to 1
        # 3 = Right stick, left to right, -1 to 1
        # 4 = Right stick, up to down, -1 to 1
        # - if event.axis == 1:
          # - print "joystick", joysticks[event.joy].get_name()
          
          # Invert axis, change range from -1 to 1 to -10 to 10
          # Also change from float to int to a string.
          # - value = str(int(event.value * 10) * -1 + 11)
          # - print "axis", event.axis, "value", value
          
          # Send it to the Arduino
          # - serialOutputToWrite = value

if __name__ == "__main__":
  main()
