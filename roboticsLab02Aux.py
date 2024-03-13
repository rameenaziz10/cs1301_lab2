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