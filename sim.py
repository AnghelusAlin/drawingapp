from turtle import Screen
import turtle
import sys
from geometry import angle_from_point, calculate_end_angle, dist, circle_centers

verbose = False

def drawGrid():
    t.speed(0)
    t.width(1)
    turtle.tracer(False)
    t.color('silver')
    for x in range(-400, 401, 10):
        t.penup()
        t.goto(x, 400)
        t.pendown()
        t.goto(x, -400)
    for y in range(-400, 401, 10):
        t.penup()
        t.goto(-400, y)
        t.pendown()
        t.goto(400, y)    
    t.width(5)
    t.color('black')
    turtle.tracer(True)

def handle_g00(command):
    t.penup()
    split = command.split()
    x = int(split[0][1:]) 
    y = int(split[1][1:]) 
    oldSpeed = t.speed()    #save the current speed
    t.speed(10)             #go as fast as possible
    t.goto(x, y)
    t.speed(oldSpeed)       #set speed back
    t.pendown()

def handle_g01(command):
    split = command.split()
    x = int(split[0][1:]) 
    y = int(split[1][1:]) 
    if len(split) > 2:
        t.speed(int(split[2][1:]))
    t.goto(x, y)

def handle_g02(command):
    current_x, current_y = t.pos()
    split = command.split()
    x = int(split[0][1:])
    y = int(split[1][1:])
    if(split[2][0] == 'R'):
        radius = int(split[2][1:])
        center_x, center_y, center2_x, center2_y = circle_centers(current_x, current_y, x, y, radius)
    else:
        center_x = int(split[2][1:])
        center_y = int(split[3][1:])
        radius = dist(current_x, current_y, center_x, center_y)
    #center is "radius" left of turtle
    angle_to_center = angle_from_point(current_x, current_y, center_x, center_y)
    t.seth(angle_to_center - 90)
    #we use seth to make center be where it should be 
    end_angle = calculate_end_angle(current_x, current_y, x, y, center_x, center_y)
    t.circle(radius, end_angle)

    #todo: IJ syntax
    
def handle_g03(command):
    current_x, current_y = t.pos()
    split = command.split()
    x = int(split[0][1:])
    y = int(split[1][1:])
    if(split[2][0] == 'R'):
        radius = int(split[2][1:])
        center_x, center_y, center2_x, center2_y = circle_centers(current_x, current_y, x, y, radius)
    else:
        center2_x = int(split[2][1:])
        center2_y = int(split[3][1:])
        radius = dist(current_x, current_y, center2_x, center2_y)
    #we know start point, end point and radius of circle
    #center is "radius" left of turtle
    
    angle_to_center = angle_from_point(current_x, current_y, center2_x, center2_y)
    t.seth(angle_to_center - 90)
    #we use seth to make center be where it should be 
    end_angle = calculate_end_angle(current_x, current_y, x, y, center2_x, center2_y)
    if(split[2][0] == 'R'):
        t.circle(radius, end_angle)
    else:
        t.circle(radius, -end_angle)

def handle_comment(command):
    if(verbose):
        print(command[1:])

t = turtle.Turtle()
def main():
    screen = Screen()
    screen.setup(800, 800)

    
    t.reset()
    t.shape('classic')
    t.speed(5)
    t.width(5)
    turtle.screensize(800, 800)

    if len(sys.argv) > 0:
        filepath = sys.argv[1]
    else:
        print("Please enter the path to a g-code file")

    f = open(filepath, "r")
    drawGrid()

    for ln in f:
        line = str(ln)
        if line.startswith("#"):
            handle_comment(line)
        elif line.startswith("G00"):
            handle_g00(line[4:])
        elif line.startswith("G01"):
            handle_g01(line[4:])
        elif line.startswith("G02"):
            handle_g02(line[4:])
        elif line.startswith("G03"):
            handle_g03(line[4:])
        else:
            print("Invalid command in file")    

    turtle.mainloop()   # in order to keep the simulation window open

if __name__ == "__main__":
    main()