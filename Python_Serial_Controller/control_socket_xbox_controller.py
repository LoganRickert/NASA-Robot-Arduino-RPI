import pygame
import serial
from pygame.locals import *
import socket
from threading import Lock
from threading import Thread
import time

#########


## Ignore all the pygame stuff.
## It's just here to get input from controller easily.

#########


# The width of the pygame window
WIN_WIDTH = 640
WIN_HEIGHT = 480

# Server address
# Host:port
server_addr = ('', 1338)

def main():
  mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  createServer(mySocket)

  delLock = False

  arduinoLock = Lock()

  global arduinoState
  arduinoState = "10"

  arduinoStateLock = Lock()

  while True:
    print 'Waiting for client...'
    client, addr = mySocket.accept()

    thread = None
    data = recvall(client)

    if data == 'arduino':
      print 'Starting arduino'
      client.send('okay')
      thread1 = Thread(target = run_client, args = (client, arduinoLock))
      thread1.start()
      thread2 = Thread(target = update_client, args = (client, arduinoLock, arduinoStateLock))
      thread2.start()
    elif data == 'phone':
      print 'Starting phone'
      thread = Thread(target = run_phone, args = (client, arduinoStateLock))
      thread.start()
    else:
      print 'Nope.', list(data)
      client.close()

def recvall(socket):
  data = "z"

  print "Got a connection!"

  while data[-1] != "\n":
    packet = socket.recv(1024)
    print list(packet)
    data += packet

  return ''.join(data[1:].split())

def stateRecvall(socket):
  data = "z"

  print "Got a connection!"

  while data[-1] != "\n":
    packet = socket.recv(1024)
    print list(packet)
    data += packet

  return data[1:].split()[-1]

def run_phone(client, arduinoStateLock):
  client.send('connected\n')

  global arduinoState
  lastArduinoState = arduinoState

  while True:
    time.sleep(.100)

    with arduinoStateLock:
      client.send(arduinoState + "\n")

def update_client(client, arduinoLock, arduinoStateLock):
  print "Running update client"

  global arduinoState

  while True:
    time.sleep(.100)

    with arduinoStateLock:
      arduinoState = stateRecvall(client)
      print ":", arduinoState

def run_client(client, arduinoLock):
  # Wait until the last serial write has finished
  serialWriteDoneA = True
  # What the new value to write is.
  serialOutputToWriteA = 0
  # What the last value wrote was.
  lastSerialOutputToWriteA = serialOutputToWriteA

  # Wait until the last serial write has finished
  serialWriteDoneB = True
  # What the new value to write is.
  serialOutputToWriteB = 0
  # What the last value wrote was.
  lastSerialOutputToWriteB = serialOutputToWriteB

  # Ignore all this stuff
  ##############
  pygame.init()
  # screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

  pygame.display.set_caption("Arduino Controller")
  game_clock = pygame.time.Clock()
  ##############

  controllers = init_controllers()

  while True:
    # Wait 60 milliseconds
    pygame.time.wait(60)

    if serialWriteDoneA and serialOutputToWriteA != lastSerialOutputToWriteA:
      serialWriteDoneA = False
      print "A" + serialOutputToWriteA
      with arduinoLock:
        client.send("A" + serialOutputToWriteA + '\n')

      lastSerialOutputToWriteA = serialOutputToWriteA
      serialWriteDoneA = True

    if serialWriteDoneB and serialOutputToWriteB != lastSerialOutputToWriteB:
      serialWriteDoneB = False
      print "B" + serialOutputToWriteB
      with arduinoLock:
        client.send("B" + serialOutputToWriteB + '\n')

      lastSerialOutputToWriteB = serialOutputToWriteB
      serialWriteDoneB = True

    # 1 - The joystick controller to read from
    # 2 - Axis          # 1 = left, up/down    # 3 = right, left/right
    # 3 - Trigger axis  # 5 = right            # 0 = left
    # 4 - Top range
    serialOutputToWriteA = getValueFromController(controllers[0], 1, 5, 20)
    serialOutputToWriteB = getValueFromController(controllers[0], 3, 2, 20)

    # Ignore all this stuff
    ##############
    pygame_events()
    ##############

def createServer(socket):
  print 'Starting server on %s:%s' % server_addr

  socket.bind(server_addr)
  socket.listen(5)

def getValueFromController(controller, axis, trigger, top_range):
  # Get the current value of the joystick. Between 1 (down) and 1 (up)
  # -1 = Flip the axis
  # 10 = increase range from -1 to 1 to -10 to 10
  axis1Pos = controller.get_axis(axis) * top_range / 2.0

  # Down is 1 and up is -1. Flip that if axis is 1.
  if axis == 1: axis1Pos *= -1

  # Get how far the trigger is pulled
  triggerMult = controller.get_axis(trigger)

  # I'm honestly not sure what this does anymore. It works though.
  triggerNormal = (((triggerMult + 1.0) / 2.0) + 1.0) / 2.0

  # Value is between 5 and 15 when trigger is at -1
  # Value is between 0 and 20 when trigger is at  1
  valueFinal = str(int(round(((axis1Pos * triggerNormal) + (top_range / 2.0)))))

  return valueFinal

def init_controllers():
  controllers = []

  for i in range(0, pygame.joystick.get_count()):
    controllers.append(pygame.joystick.Joystick(i))
    controllers[-1].init()

    print "Adding joystick", controllers[-1].get_name()

  return controllers

def pygame_events():
  # Ignore this stuff
  for event in pygame.event.get():
    if event.type == QUIT:
      print "Exiting the window..."
      exit(0)
    elif event.type == KEYDOWN:
      print "Key down:", event.key
      if event.key == 'c':
        print "Exiting the window..."
        exit(0)
      # 1 = Left stick, up to down, -1 to 1
      # 2 = Left stick, left to right, -1 to 1
      # 3 = Right stick, left to right, -1 to 1
      # 4 = Right stick, up to down, -1 to 1

if __name__ == "__main__":
  main()
