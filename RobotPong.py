from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
name = "R2-D2"
robot = Create3(Bluetooth(name))   # Put robot name here.

# IR Sensor Angles
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

# --------------------------------------------------------
# Implement the first two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------

#GLOBALS
BUTTONPRESS = False

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_touched(robot):
    global BUTTONPRESS
    BUTTONPRESS = True
    

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global BUTTONPRESS
    BUTTONPRESS = True

# --------------------------------------------------------
# Implement robotPong() so that the robot:
#     Sets the initial light to cyan.
#     Moves in a straight line at 15 units/s.
#     CONTINUOUSLY checks IR readings for nearby walls.
#     If the closest wall is <= 20 units away,
#         Momentarily stop.
#         Reflect its direction based on the angle of the wall.
#         Change the light from cyan to magenta, or vice versa.
# --------------------------------------------------------

@event(robot.when_play)
async def robotPong(robot):
    global BUTTONPRESS
    """
    Use the following two lines somewhere in your code to calculate the
    angle and direction of reflection from a list of IR readings:
    """
    while not BUTTONPRESS:
        speed = 15
        
        ir_readings = (await robot.get_ir_proximity()).sensors
        (approx_dist, approx_angle) = angleOfClosestWall(ir_readings)
        (direction, turningAngle) = calculateReflectionAngle(approx_angle)
        if approx_dist < 20:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(255,0,255)
            if direction == "right":
                await robot.turn_right(turningAngle)
            if direction == "left":
                await robot.turn_left(turningAngle)
        else:
            await robot.set_lights_rgb(0,255,255)
            await robot.set_wheel_speeds(speed, speed)
        if BUTTONPRESS:
            await robot.set_lights_rgb(255,0,0)
            await robot.set_wheel_speeds(0,0)
        



    """
    Then, if the closest wall is less than 20 cm away, use the
    direction and the turningAngle to determine how to rotate the robot to
    reflect.
    """
    

def angleOfClosestWall(readings):
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

# start the robot
robot.play()
