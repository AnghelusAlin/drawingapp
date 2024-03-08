import math

def angle_from_point(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def calculate_end_angle(x1, y1, x2, y2, center_x, center_y):
    # Calculate differences in coordinates
    delta_x = x2 - center_x
    delta_y = y2 - center_y
    ref_x = x1 - center_x
    ref_y = y1 - center_y

    # Calculate angles in radians
    angle_arbitrary = math.atan2(delta_y, delta_x)
    angle_reference = math.atan2(ref_y, ref_x)

    # Calculate the angle difference between the arbitrary point and the reference point
    angle = math.degrees(angle_arbitrary - angle_reference)
    if angle == 0:
        angle = 360
    return angle

def circle_centers(x1, y1, x2, y2, radius):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    # m is the midpoint between the two given points
    d1 = dist(x1, y1, mx, my) 
    d1_2 = pow(d1, 2)
    radius_2 = pow(radius, 2)
    if radius_2 < d1_2:
        print("Radius too small for circle")
        print (str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(radius))
        #should do this with exceptions
        return
    #distance between middle and second point
    dmc = math.sqrt(radius_2 - d1_2)
    #Pythagorean theorem to get the distance from middle to center of circle
    #this is also the distance to the other center, since this is symmetrical with the axis P1-P2
    a = math.atan2(y2 - y1, x2 - x1)    
    #angle between horizontal axis and the line between the two points
    
    b = math.asin(dmc/radius)
    c = a - b
    #angle between horizontal axis and the line between the first point and the circle center
    rx = radius * math.cos(c)
    ry = radius * math.sin(c)
    center1_x = x1 + rx
    center1_y = y1 + ry

    center2_x = 2 * mx - center1_x
    center2_y = 2 * my - center1_y

    #center1 is clockwise, center2 is counterclockwise
    return center1_x, center1_y, center2_x, center2_y

def dist(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(pow(dx, 2) + pow(dy,2))

# "gui" functions are made for the coordinate system of the tkinter canvas
# tkinter canvas has (0, 0) in the top left corner, and y increases downwards
# turtle canvas has (0, 0) in the center, and y increases upwards

def angle_from_point_gui(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y1 - y2  # Reversed y-coordinates
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def calculate_end_angle_gui(x1, y1, x2, y2, center_x, center_y):
    # Calculate differences in coordinates
    delta_x = x2 - center_x
    delta_y = center_y - y2  # Reversed y-coordinates
    ref_x = x1 - center_x
    ref_y = center_y - y1  # Reversed y-coordinates

    # Calculate angles in radians
    angle_arbitrary = math.atan2(delta_y, delta_x)
    angle_reference = math.atan2(ref_y, ref_x)

    # Calculate the angle difference between the arbitrary point and the reference point
    angle = math.degrees(angle_arbitrary - angle_reference)
    if angle == 0:
        angle = 360
    return angle

def circle_centers_gui(x1, y1, x2, y2, radius):
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    # m is the midpoint between the two given points
    d1 = dist(x1, y1, mx, my) 
    d1_2 = pow(d1, 2)
    radius_2 = pow(radius, 2)
    if radius_2 < d1_2:
        print("Radius too small for circle")
        return  # Return without calculation

    # Distance between middle and second point
    dmc = math.sqrt(radius_2 - d1_2)
    # Pythagorean theorem to get the distance from middle to center of circle
    # This is also the distance to the other center, since this is symmetrical with the axis P1-P2
    a = math.atan2(y1 - y2, x2 - x1)  # Reversed y-coordinates
    # Angle between horizontal axis and the line between the two points

    b = math.asin(dmc / radius)
    c = a - b
    # Angle between horizontal axis and the line between the first point and the circle center
    rx = radius * math.cos(c)
    ry = radius * math.sin(c)
    center1_x = x1 + rx
    center1_y = y1 - ry  # Reversed y-coordinates

    center2_x = 2 * mx - center1_x
    center2_y = 2 * my - center1_y

    # center1 is clockwise, center2 is counterclockwise
    return center1_x, center1_y, center2_x, center2_y
