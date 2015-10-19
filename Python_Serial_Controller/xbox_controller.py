import pygame
from pygame.locals import *

WIN_WIDTH = 640
WIN_HEIGHT = 480

def main():
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
    game_clock.tick(60)
    
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
        if event.axis == 1:
          print "joystick", joysticks[event.joy].get_name()
          print "axis", event.axis, "value", event.value

if __name__ == "__main__":
  main()
