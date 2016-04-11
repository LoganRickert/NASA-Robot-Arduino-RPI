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

