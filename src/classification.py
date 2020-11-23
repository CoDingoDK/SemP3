import math


def point_to_point_angle(origin, point):
    degrees = int(math.degrees(math.atan2(point[1] - origin[1], point[0] - origin[0])))
    if 45 >= math.fabs(degrees):
        print(f"\r{degrees} is right",end="")
    elif -45 >= degrees > -135:
        print(f"\r{degrees} is up",end="")
    elif 135 <= math.fabs(degrees):
        print(f"\r{degrees} is left",end="")
    elif 45 <= degrees < 135:
        print(f"\r{degrees} is down",end="")
