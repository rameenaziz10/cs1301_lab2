from time import perf_counter
def angleOfClosestWall(readings):
    """Remember that this function can be autograded!"""
    IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
    max = 0 
    closest = 0
    for index, i in enumerate(readings):
        if i > max:
            max = i
            closest = IR_ANGLES[index]
    max = 4095 / (max + 1)
    max = round(max, 3)
    return max, closest

def calculateReflectionAngle(angle):
    direc = ""
    if angle >= 0:
        direc = "left"
        angle = 180 - 2 * angle
    elif angle < 0:
        direc = "right"
        angle = 180 + 2 * angle
    angle = round(angle, 3)
    return direc, angle

import math as m
def farthestDistance(currPosition, positions):
    x1, y1 = currPosition
    maxdist = 0
    maxpos = (0,)
    for tup in positions:
        x2, y2 = tup
        distance = m.sqrt(m.fabs((x2 - x1)**2  + (y2 - y1)**2))
        print(distance)
        if distance > maxdist:
            maxdist = distance
            maxpos = x2, y2
    return maxpos   

def movementDirection(readings):
    max = 0
    sensorIndex = -1
    for i in range(len(readings)):
        if readings[i] > max:
            max = readings[i]
            sensorIndex = i
    if sensorIndex in [0, 1, 2]: 
        direc = "clockwise"                            
    elif sensorIndex in [4,5,6]:  
        direc = "counterclockwise"    
    return direc

def checkPositionArrived(current_position, destination, threshold):
    
    x1, y1 = current_position
    x2, y2 = destination
    distance = m.sqrt(m.fabs((x2 - x1)**2  + (y2 - y1)**2))
    if distance <= threshold:
        return True
    else:
        return False
time1 = perf_counter()
print(checkPositionArrived((7,2), (0,0), 5))
time2 = perf_counter()
timeelapsed = time2 - time1
print(timeelapsed)
