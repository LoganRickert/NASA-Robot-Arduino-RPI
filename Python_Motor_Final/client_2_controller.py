import pygame
from pygame.locals import *
import socket
import math
import time
import bz2
import binascii
import ast

from threading import Thread

WIN_WIDTH = 1024
WIN_HEIGHT = 576

def getNewImage():
    global picture_ready
    global stop
    global oldData

    oldData = ''
    stop = False
    global whichCamera
    global totalCams

    imageClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    imageClient.connect(('192.168.1.109', 1338))
    imageClient.send('superawesomesecurepassword\n')
    print ':', recvall(imageClient)

    curTime = time.time()
    imageClient.send('R' + str(whichCamera) + '\n')
    data = ''.join(recvall(imageClient))

    go = True

    while go:
        if picture_ready:
            #print 'took:', time.time() - curTime
            curTime = time.time()

            if oldData != data:
                picture_ready = False
                update_image_thread = Thread(
                    target=updateImage,
                    args=(data,)
                )
                #print 'starting update thread'
                update_image_thread.start()

            # whichCamera = (whichCamera + 1) % totalCams
            imageClient.send('R' + str(whichCamera) + '\n')
            oldData = data
            data = ''.join(recvall(imageClient))

        if stop:
            imageClient.close()
            go = False
            
        time.sleep(0.05)

def updateImage(data):
    x_scale = 4
    y_scale = 4

    current = time.time()
    image = bz2.decompress(binascii.unhexlify(data))
    #print "sent:", len(data)
    #print "comp:", len(binascii.unhexlify(data))
    #print "pixels:", len(image)
    image = ast.literal_eval(image)

    snapshot = pygame.surface.Surface((640, 360), 0)
    pxarrayA = pygame.PixelArray(snapshot)

    lenx = len(pxarrayA)
    leny = len(pxarrayA[0])

    #print 'lenx:', lenx
    #print 'leny:', leny

    color_end = []

    for x in range(0, lenx):
      current_color = []
      for y in range(0, leny):
        money_shot = (leny / y_scale) * (x / x_scale) + (y / y_scale)
        if (money_shot) < len(image):
          color = image[money_shot]
          div = 8
          pxarrayA[x, y] = (color * div, color * div, color * div)

    del pxarrayA

    global picture
    picture = snapshot
    global picture_ready
    picture_ready = True
    print 'picture ready!'

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
  #imageSurface = pygame.image.load('3_points.png')
  #screen.blit(imageSurface, ((WIN_WIDTH - 640) - 20, 20))

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

  global picture
  if picture != None:
    screen.blit(picture, (364, 20))

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
  last_lefta = 0
  last_leftb = 0
  last_righta = 0
  last_rightb = 0
  last_raw_a = 0
  last_raw_b = 0
  last_raw_t_a = 0
  last_raw_t_b = 0

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

  count = 0

  getNewImage_thread = Thread(
      target=getNewImage
  )
  
  print 'starting update thread'
  getNewImage_thread.start()

  global picture
  picture = None
  global picture_ready
  picture_ready = True

  global whichCamera
  whichCamera = 0
  global totalCams
  totalCams = 1
  
  while should_continue:
    game_clock.tick(60)

    updateGUI(screen, font, font_small, speed, turning, turning_degree, buckets_speed, camera_feed, 
      lt, rt, bl, br, fl, fr)
    
    for event in pygame.event.get():
      if event.type == QUIT:
        print "Exiting the window..."
        pygame.quit()
        should_continue = False
        global stop
        stop = True
      elif event.type == KEYDOWN:
        print "Key down:", event.key
      elif event.type == JOYBUTTONDOWN:
          if event.button == 2:
              # x button
              client.send('G' + '20' + '\n')
              pass
          elif event.button == 4:
              is_left_button = True
          elif event.button == 5:
              is_right_button = True
      elif event.type == JOYBUTTONUP:
          if event.button == 0:
            print 'Changing camera feeds'
            whichCamera = (whichCamera + 1) % totalCams
          if event.button == 2:
              # x button
              client.send('G' + '10' + '\n')
              pass
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
          # Buckets
          last_raw_a = joysticks[0].get_axis(event.axis)
          last_raw_b = joysticks[1].get_axis(event.axis)

          buckets_speed = getValueFromController(last_raw_b, trigger_value, 20, True)
          value1 = buckets_speed
          if last_lefta != value1:
              client.send('F' + str(value1) + '\n')
              last_lefta = value1
              print 'left_buckets:', value1

          # Front/back wheels
          speed = getValueFromController(last_raw_a, trigger_value, 20, True)
          value1 = speed
          if last_leftb != value1:
              client.send('A' + str(value1) + '\n')
              last_leftb = value1
              print 'left:', value1

        if event.axis == 3:
          last_raw_t_b = joysticks[1].get_axis(event.axis)

          # Buckets actuator
          turningb = getValueFromController(last_raw_t_b, trigger_value, 20)
          valueb = turningb

          if last_rightb != valueb:
            client.send('I' + str(valueb) + '\n')
            last_rightb = valueb
            print 'left controller:', valueb

        if event.axis == 4:
          last_raw_t_a = joysticks[0].get_axis(event.axis)

          # Steering actuator
          turninga = getValueFromController(last_raw_t_a, trigger_value, 20)
          valuea = turninga

          if last_righta != valuea:
            client.send('H' + str(valuea) + '\n')
            last_righta = valuea
            print 'right controller:', valuea

        if event.axis == 2:
          trigger_value_a = -joysticks[0].get_axis(event.axis)
          trigger_value_b = -joysticks[1].get_axis(event.axis)

          # Adjustment for speed
          buckets_speed = getValueFromController(last_raw_b, trigger_value_b, 20, True)
          value1 = buckets_speed

          if last_leftb != value1:
              print 'sending F'
              client.send('F' + str(value1) + '\n')
              last_leftb = value1
              print 'triggers-left:', value1      

          speed = getValueFromController(last_raw_a, trigger_value_a, 20, True)
          value1 = speed
          if last_lefta != value1:
              client.send('A' + str(value1) + '\n')
              last_lefta = value1
              print 'triggers-left:', value1
        
          turning = getValueFromController(last_raw_t_a, trigger_value_a, 20)
          value2 = turning

          if last_righta != value2:
            client.send('H' + str(value2) + '\n')
            last_righta = value2
            print 'triggers-right-act:', value2  

          turning = getValueFromController(last_raw_t_b, trigger_value_b, 20)
          value2 = turning       
          if last_rightb != value2:
            client.send('I' + str(value2) + '\n')
            last_rightb = value2
            print 'triggers-right:', value2

if __name__ == "__main__":
  main()
