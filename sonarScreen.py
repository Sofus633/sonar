import serial
import time
import pygame
import math
import random
import ast

SCREEN_SIZE = [1000, 800]
ZOOM = 1.2
maxrotation = 180
nbpoint = 100
precision = maxrotation // nbpoint
minnoise = 480
maxnoise = 500
screen = pygame.display.set_mode(SCREEN_SIZE)

def zoom_down():
    global ZOOM
    ZOOM -= .05
    print(f"Zoom of point set to :{ZOOM}")
def zoom_up():
    global ZOOM
    ZOOM += .05
    print(f"Zoom of point set to :{ZOOM}")

def nbpoint_up():
    global nbpoint, precision, maxrotation
    nbpoint += 1;
    precision = maxrotation // nbpoint
    print(f"Number of point set to :{nbpoint}")
def nbpoint_down():
    global nbpoint, precision, maxrotation
    nbpoint -= 1;
    precision = maxrotation // nbpoint
    print(f"Number of point set to :{nbpoint}")
def maxrotatio_up():
    global nbpoint, precision, maxrotation
    maxrotation += 1;
    precision = maxrotation // nbpoint
    print(f"Rotation set to :{maxrotation}")
def  maxrotation_down():
    global nbpoint, precision, maxrotation
    maxrotation -= 1;
    precision = maxrotation // nbpoint
    print(f"Rotation set to :{maxrotation}")

def random_test():
    global precision, nbpoint, maxrotation, minnoise, maxnoise
    points = []
    for angle in range(0, maxrotation, precision):
        points.append((math.cos(math.radians(angle)) * random.randint(minnoise, maxnoise), math.sin(math.radians(angle)) * random.randint(minnoise, maxnoise)))
    return points

def act_screen():
    global points, arduino
    #points = retrive_arr_pts(arduino) 
    #todo Remove
    points = random_test()
    #THIS

def retrive_arr_pts(arduino):
    global points, points_idc
    while (arduino.in_waiting < 0):
        pass
    header = arduino.readline().decode('utf-8').strip();
    if (header != "Entry Start :"):
        return retrive_arr_pts(arduino)
    mess = arduino.readline().decode('utf-8').strip();
    angle = arduino.readline().decode('utf-8').strip();
    return ast.literal_eval('[' + mess + ']'), int(angle)

def trace_lines(points, origin):
    origin = [origin[0]* ZOOM, origin[1] * ZOOM]
    for i in range(len(points)):
        dest = ((origin[0] + points[i][0])*ZOOM, (origin[1] + points[i][1])*ZOOM)
        pygame.draw.line(screen, (255, 0, 0), origin ,dest)

def trace_inter_lines(points, origin):
    points_l = len(points)
    for i in range(0, len(points)):
         if (i + 1 < points_l):
            p1 = ((origin[0] + points[i][0]) * ZOOM, (origin[1] + points[i][1]) * ZOOM)
            p2 = ((origin[0] + points[i+1][0]) * ZOOM, (origin[1] + points[i+1][1]) * ZOOM)
            pygame.draw.line(screen, (255, 0, 0), p1, p2)

def add_dic(elem, dic, tab):
    print(elem[1], dic)
    if elem[1] in dic.keys():
        if dic[elem[1]] == elem[0]:
            print("fine")
            return
        else:
            dic[elem[1]] = elem[0]
            print("change detected")
    else:
        dic[elem[1]] = elem[0]
        tab.append(elem[0])
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
time.sleep(2)

key_bindings = {
    pygame.K_t : zoom_up,
    pygame.K_y : zoom_down,
    pygame.K_g : nbpoint_up,
    pygame.K_h : nbpoint_down,
    pygame.K_b : maxrotatio_up,
    pygame.K_n : maxrotation_down,
    pygame.K_r : act_screen
}
origin = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
points = []
points_dic = {}
#for angle in range(0, 180, 1):
#    print(angle)
#    print(((math.cos(angle) * random.randint(500, 1000), math.sin(angle) * random.randint(500, 1000))))
#    points.append((math.cos(math.radians(angle)) * random.randint(290, 300), math.sin(math.radians(angle)) * random.randint(290, 300)))

#points.append((math.cos(180) * random.randint(0, 100), math.sin(180)* random.randint(0, 100)))
#points = [(x, 100) for x in range(0, 1000, 10)]
#trace_inter_lines(points, origin)
#pygame.display.flip()

retrive_arr_pts(arduino)
#main loop
running = True
while running:
    add_dic(retrive_arr_pts(arduino), points_dic, points)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
             if event.key in key_bindings: 
                key_bindings[event.key]()
                screen.fill(0)
                trace_lines(points, origin)
                trace_inter_lines(points, origin)
                pygame.display.flip()


arduino.close()
