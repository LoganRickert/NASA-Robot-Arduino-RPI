import pygame
from pygame.locals import *
import socket
import math

WIN_WIDTH = 1024
WIN_HEIGHT = 576

def getValueFromController(axis_value, trigger, top_range, reverse=False):
    # Get the current value of the joystick. Between 1 (down) and 1 (up)
    # -1 = Flip the axis
    # 10 = increase range from -1 to 1 to -10 to 10
    axis1Pos = axis_value * top_range / 2.0

    # Down is 1 and up is -1. Flip that if axis is 1.
    if reverse: axis1Pos *= -1

    # Trigger value. Please make sure it's from 0 to 1.
    triggerMult = trigger

    # I'm honestly not sure what this does anymore. It works though.
    triggerNormal = ((triggerMult) + 1.0) / 2.0

    # Value is between 5 and 15 when trigger is at -1
    # Value is between 0 and 20 when trigger is at  1
    valueFinal = int(round(((axis1Pos * triggerNormal) + (top_range / 2.0))))

    return valueFinal

def recvall(client_socket):
    data = "z"
    
    print "Recving data!"

    while data[-1] != "\n":
        packet = client_socket.recv(1024)
        data += packet

    data = data[1:] # We need the z so we can check data[-1]
                    # It will give out of bounce error otherwise.

    # print 'Recving:', data.split('\n')[:-1]

    return data.split('\n')[:-1]

def draw_pie(surface, cx, cy, r, start_angle, end_angle, color):
  #Start list of polygon points
  p = [(cx,cy)]

  start_angle -= 90
  end_angle -= 90

  ### I need to change this crappy code and make it so cos / sin is only
  ### calculated once.
  #Get points on arc
  for n in range(start_angle, end_angle):
      x = cx + int(r*math.cos(n*math.pi/180))
      y = cy + int(r*math.sin(n*math.pi/180))
      p.append((x,y))

      x = cx + int(r*math.cos((n + 0.5)*math.pi/180))
      y = cy + int(r*math.sin((n + 0.5)*math.pi/180))
      p.append((x,y))
  p.append((cx,cy))

  #Draw pie segment
  if len(p) > 2:
      pygame.draw.polygon(surface,color,p)

def updateGUI(screen, font, font_small,
  speed, turning, turning_degree, buckets_speed, camera_feed, 
  lt, rt, bl, br, fl, fr):
  
  # How far the circle should be turned.
  speed_mat_pos = [0, 0]
  turning_mat_pos = [0, 0]
  buckets_speed_mat_pos = [0, 0]
  posC = [0, 0]

  # Starting place for speed of sticks
  speed_position = int((math.fabs(10 - speed) / 10) * 180)
  turning_position = int((math.fabs(10 - turning) / 10) * 180)
  buckets_speed_position = int((math.fabs(10 - buckets_speed) / 10) * 180)

  # This is doing something.
  if speed > 10: speed_mat_pos[1] = speed_position
  else: speed_mat_pos[0] = -speed_position

  if turning > 10: turning_mat_pos[1] = turning_position
  else: turning_mat_pos[0] = -turning_position

  if buckets_speed > 10: buckets_speed_mat_pos[1] = buckets_speed_position
  else: buckets_speed_mat_pos[0] = -buckets_speed_position

  # Fill the screen black
  screen.fill((0, 0, 0))

  # Put the image onto the screen
  imageSurface = pygame.image.load('3_points.png')
  screen.blit(imageSurface, ((WIN_WIDTH - 640) - 20, 20))

  # Surfaces for circles
  circleSurfaces = pygame.surface.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA, 32)
  circleSurfaces = circleSurfaces.convert_alpha()

  draw_pie(circleSurfaces, 95, 130, 71, speed_mat_pos[0], speed_mat_pos[1], (81, 171, 203))
  draw_pie(circleSurfaces, 265, 130, 71, turning_mat_pos[0], turning_mat_pos[1], (81, 171, 203))
  draw_pie(circleSurfaces, 178, 280, 71, -45, 130, (81, 171, 203))
  draw_pie(circleSurfaces, 458, 479, 71, buckets_speed_mat_pos[0], buckets_speed_mat_pos[1], (81, 171, 203))

  # For speed of motors
  pygame.draw.rect(circleSurfaces, (81, 171, 203), (83, 422 + int(105 * 0.5), 25, 105))
  pygame.draw.rect(circleSurfaces, (81, 171, 203), (124, 422 + int(105 * 0.25), 25, 105))
  pygame.draw.rect(circleSurfaces, (39, 147, 96), (165, 422 + int(105 * 0.35), 25, 105))
  pygame.draw.rect(circleSurfaces, (39, 147, 96), (206, 422 + int(105 * 0.75), 25, 105))
  pygame.draw.rect(circleSurfaces, (39, 147, 96), (247, 422 + int(105 * 0.85), 25, 105))
  pygame.draw.rect(circleSurfaces, (39, 147, 96), (288, 422 + int(105 * 0.5), 25, 105))

  # Add the circle surface to screen
  screen.blit(circleSurfaces, (0, 0))

  # Add the background to the screen
  bgSurface = pygame.image.load('pygamebackground.png')
  screen.blit(bgSurface, (0, 0))

  # Add the texts
  text = font.render(str(speed - 10), 1, (255, 255, 255))
  textpos = text.get_rect(centerx = 95, centery = 132)
  screen.blit(text, textpos)

  text = font.render(str(turning - 10), 1, (255, 255, 255))
  textpos = text.get_rect(centerx = 265, centery = 132)
  screen.blit(text, textpos)

  text = font.render('45', 1, (255, 255, 255))
  textpos = text.get_rect(centerx = 178, centery = 282)
  screen.blit(text, textpos)

  text = font.render(str(buckets_speed - 10), 1, (255, 255, 255))
  textpos = text.get_rect(centerx = 459, centery = 481)
  screen.blit(text, textpos)

  # Display the new image.
  pygame.display.flip()

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
  
  trigger_value = 0
  last_left = 0
  last_right = 0
  last_left_raw = 0
  last_right_raw = 0

  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(('192.168.1.109', 1338))
  client.send('superawesomesecurepassword\n')

  print recvall(client)

  should_continue = True

  pygame.font.init()
  font = pygame.font.Font(None, 30)
  font_small = pygame.font.Font(None, 26)

  speed = 0
  turning = 0
  turning_degree = 0
  buckets_speed = 0
  camera_feed = 0
  lt = 0
  rt = 0
  bl = 0
  br = 0
  fl = 0
  fr = 0

  is_left_button = False
  is_right_button = False

  while should_continue:
    game_clock.tick(60)

    updateGUI(screen, font, font_small, speed, turning, turning_degree, buckets_speed, camera_feed, 
      lt, rt, bl, br, fl, fr)
    
    for event in pygame.event.get():
      print event.type
      if event.type == QUIT:
        print "Exiting the window..."
        pygame.quit()
        should_continue = False
      elif event.type == KEYDOWN:
        print "Key down:", event.key
      elif event.type == JOYBUTTONDOWN:
          if event.button == 2:
              # x button
              client.send('G' + '15' + '\n')
          elif event.button == 4:
              is_left_button = True
          elif event.button == 5:
              is_right_button = True
      elif event.type == JOYBUTTONUP:
          if event.button == 2:
              # x button
              client.send('G' + '10' + '\n')
          elif event.button == 4:
              is_left_button = False
          elif event.button == 5:
              is_right_button = False
      elif event.type == JOYAXISMOTION:
        # 1 = Left stick, up to down, -1 to 1
        # -1 = Left stick, up to down, -1 to 1     
        # 2 = Left stick, left to right, -1 to 1
        # -2 = Left trigger 1 to 0
        # -2 = Right trigger 0 to 1
        # 3 = Right stick, left to right, -1 to
        # -3 = Right stick, up to down, -1 to 1
        # 4 = Right stick, up to down, -1 to 1
        # -4 = Right stick, left to right, -1 to 1
        #print event.axis
        if event.axis == 1:
          last_left_raw = event.value
          if is_left_button:
              buckets_speed = getValueFromController(last_left_raw, trigger_value, 20, True)
              value1 = buckets_speed
              if last_left != value1:
                  client.send('F' + str(value1) + '\n')
                  last_left = value1
                  print 'left_buckets:', value1
          else:
              speed = getValueFromController(last_left_raw, trigger_value, 20, True)
              value1 = speed
              if last_left != value1:
                  client.send('A' + str(value1) + '\n')
                  last_left = value1
                  print 'left:', value1

        if event.axis == 4:
          last_right_raw = event.value
          if is_right_button:
              turning = getValueFromController(event.value, trigger_value, 20)
              value1 = turning

              if last_right != value1:
                client.send('I' + str(value1) + '\n')
                last_right = value1
                print 'right:', value1
          else:
              turning = getValueFromController(event.value, trigger_value, 20)
              value1 = turning

              if last_right != value1:
                client.send('H' + str(value1) + '\n')
                last_right = value1
                print 'right:', value1

        if event.axis == 2:
          trigger_value = -event.value
          if is_left_button:
              buckets_speed = getValueFromController(last_left_raw, trigger_value, 20, True)
              value1 = buckets_speed

              if last_left != value1:
                  print 'sending F'
                  client.send('F' + str(value1) + '\n')
                  last_left = value1
                  print 'triggers-left:', value1              
          else:
              speed = getValueFromController(last_left_raw, trigger_value, 20, True)
              value1 = speed
              if last_left != value1:
                  client.send('A' + str(value1) + '\n')
                  last_left = value1
                  print 'triggers-left:', value1
        
          turning = getValueFromController(last_right_raw, trigger_value, 20)
          value2 = turning

          if is_right_button:
              if last_right != value2:
                client.send('I' + str(value2) + '\n')
                last_right = value2
                print 'triggers-right-act:', value2         
          else:
              if last_right != value2:
                client.send('H' + str(value2) + '\n')
                last_right = value2
                print 'triggers-right:', value2



if __name__ == "__main__":
  main()
