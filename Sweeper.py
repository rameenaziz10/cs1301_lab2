from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
import math as m
name = "XJ-9"
robot = Create3(Bluetooth(name))   # Put robot name here.

# --------------------------------------------------------
# Global Variables - feel free to add your own as necessary
# --------------------------------------------------------

# Behavorial
HAS_COLLIDED = False     # The robot has collided with a wall.
HAS_EXPLORED = False     # The robot has finished exploring the box.
HAS_SWEPT = False        # The robot has finished sweeping, and
                         # has arrived at its final destination.

# Spatial Awareness
SENSOR2CHECK = 0         # The index of the sensor that corresponds 
                         # with the closest side wall,
                         # either 0 for left-most or -1 for right-most.
ROTATION_DIR = 0         # The direction the robot needs to explore.
CORNERS = []             # A list that stores all the corners as the robot explores.
DESTINATION = ()         # The point that is the farthest away from the robot.
                         # This point becomes the robot's final destination.

# Constants - Do not change.
ARRIVAL_THRESHOLD = 5    # We say that the robot has arrived at its final
                         # destination if the distance between the robot's
                         # position and the location of the final destination
                         # is less than or equal to this value.
SPEED = 10               # The speed at which the robot should normally move.
ROBOT_MOVE_DISTANCE = 15 # The distance by which the robot needs to move 
                         # to the side to sweep a new column of the box.
BUTTONPRESS = False
AT_ORIGIN = False
# --------------------------------------------------------
# Implement these three helper functions so that they
# can be used later on.
# --------------------------------------------------------
from math import sqrt as s
# Helper Function 1
def farthestDistance(currPosition, positions):
    x1, y1 = currPosition
    maxdist = 0
    maxpos = (0,)
    for tup in positions:
        x2, y2 = tup
        distance = m.sqrt(m.fabs((x2 - x1)**2  + (y2 - y1)**2))
        if distance > maxdist:
            maxdist = distance
            maxpos = x2, y2
    return maxpos

# Helper Function 2
def movementDirection(readings):
    max = 0
    sensorIndex = -1
    direc = "clockwise"
    for i in range(len(readings)):
        if readings[i] >= 20:
            if readings[i] > max:
                max = readings[i]
                sensorIndex = i
    if sensorIndex in [0, 1, 2]: 
        direc = "clockwise"                            
            
    elif sensorIndex in [4,5,6]:  
        direc = "counterclockwise" 
    return direc        
            

# Helper Function 3
def checkPositionArrived(current_position, destination, threshold):
    x1, y1 = current_position
    x2, y2 = destination
    distance = m.sqrt(m.fabs((x2 - x1)**2  + (y2 - y1)**2))
    if distance <= threshold:
        return True
    else:
        return False

# --------------------------------------------------------
# Implement the these two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_touched(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True


# --------------------------------------------------------
# Implement play such that the robot:
#     Resets its navigational coordinate system.
#     Uses movementDirection() to determine which direction
#         the robot should plan to explore the box.
#     Sets SENSOR2CHECK and ROTATION_DIR depending on whether
#         the robot is going to move clockwise or counterclockwise.
#     Sets the wheel speed to SPEED
#     Calls sweep() and explore() inside of a while loop.
#         If the robot has not finished exploring, call explore()
#         If the robot has finished exploring, call sweep()
#     Stops execution after a collision or after the final
#         destination is reached.
# --------------------------------------------------------

@event(robot.when_play)
async def play(robot):
    global HAS_COLLIDED, HAS_EXPLORED, HAS_SWEPT, SENSOR2CHECK
    global ROTATION_DIR, CORNERS, DESTINATION, ARRIVAL_THRESHOLD
    global SPEED, ROBOT_MOVE_DISTANCE
    #find position and sensor readings % reset navigation
    readings = (await robot.get_ir_proximity()).sensors
    ROTATION_DIR = movementDirection(readings)
    if ROTATION_DIR == "clockwise":
        SENSOR2CHECK = 0
    else:
        SENSOR2CHECK = 6
    await robot.reset_navigation()
    #assign global variables based off of proximity to walls
    
    #set wheel speed
    await robot.set_wheel_speeds(SPEED, SPEED)
    #use explore and sweep functions
    while not HAS_EXPLORED:
        
        if HAS_COLLIDED:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(255,0,0)
            print('collided :(')
            break
        await explore(robot)
        if HAS_EXPLORED:
            await robot.set_wheel_speeds(0,0)
            print("finished exploring!")
    
    while not HAS_SWEPT:
        if HAS_COLLIDED:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(255,0,0)
            print('collided :(')
            break
        await sweep(robot)
        if HAS_SWEPT: 
            print("finished sweeping")
    readings = (await robot.get_ir_proximity()).sensors
    ROTATION_DIR = movementDirection(readings)
    if ROTATION_DIR == "clockwise":
        SENSOR2CHECK = 0
    else:
        SENSOR2CHECK = 6
    while not AT_ORIGIN:
        if HAS_COLLIDED:
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights_rgb(255,0,0)
            print('collided :(')
            break
        else:
            await getToOrigin(robot)
    if AT_ORIGIN:
        current_position = await robot.get_position()
        pos = current_position.x, current_position.y
        print(pos)
        print("welcome back")
        await robot.turn_right(360)
        
        



# --------------------------------------------------------
# Implement explore such that the robot:
#     Finds the front and side proximity to a wall.
#     If there is a wall within 10 units in front,
#         stop, turn 90 degrees, and continue.
#     When all four corners have been found, determine
#         the furthest corner from the robot with farthestDistance() 
#     Auto-aligns with the side boundary if the robot drifts
#         away from the side wall.
# --------------------------------------------------------

async def explore(robot):
    global HAS_COLLIDED, HAS_EXPLORED, HAS_SWEPT, SENSOR2CHECK
    global ROTATION_DIR, CORNERS, DESTINATION, ARRIVAL_THRESHOLD
    global SPEED, ROBOT_MOVE_DISTANCE
    current_position = await robot.get_position()
    pos = current_position.x, current_position.y
    readings = (await robot.get_ir_proximity()).sensors
    
    middle = readings[3]
    dist = 4095 / (middle + 1)
    
    if dist <= 10:

        await robot.set_wheel_speeds(0,0)
        CORNERS.append(pos)
        if len(CORNERS) == 4:
            DESTINATION = farthestDistance(pos,CORNERS)
            HAS_EXPLORED = True
        else:
            if ROTATION_DIR == "clockwise":
                await robot.turn_right(90)
            else:
                await robot.turn_left(90)

        await robot.set_wheel_speeds(SPEED,SPEED)
    sidesens = readings[SENSOR2CHECK]
    sidedist = 4095 / (sidesens + 1)
    if sidedist <= 5 or sidedist > 10:
        if ROTATION_DIR == "clockwise":
            if sidedist <= 5:
                await robot.turn_right(3)
            if sidedist > 10:
                await robot.turn_left(3)
        else:
            if sidedist <= 5:
                await robot.turn_left(3)
            if sidedist > 10:
                await robot.turn_right(3)
        await robot.set_wheel_speeds(SPEED, SPEED)
    

    
            




# --------------------------------------------------------
# Implement sweep such that the robot:
#     Checks if it has reached its final destination with
#         checkPositionArrived()
#     If the robot did reach its destination, stop, set
#         lights to green, and play a happy tune.
#     Else, if the robot's front proximity to a wall is <= 10 units,
#         stop, turn 90 degrees, move forwards by ROBOT_MOVE_DISTANCE,
#         turn 90 degrees again, and start again.
# --------------------------------------------------------

async def sweep(robot): # Change tolerance for sweep and changed the baby steps
    global HAS_COLLIDED, HAS_EXPLORED, HAS_SWEPT, SENSOR2CHECK
    global ROTATION_DIR, CORNERS, DESTINATION, ARRIVAL_THRESHOLD
    global SPEED, ROBOT_MOVE_DISTANCE
    current_position = await robot.get_position()
    pos = current_position.x, current_position.y
    readings = (await robot.get_ir_proximity()).sensors
    
    middle = readings[3]
    dist = 4095 / (middle + 1)
    middle = readings[3]
    dist = 4095 / (middle + 1)
    if checkPositionArrived(pos, DESTINATION, ARRIVAL_THRESHOLD):
        await robot.set_wheel_speeds(0,0)
        await robot.set_lights_rgb(0,255,0)
        await robot.play_note(Note.D5, .5)
        await robot.play_note(Note.F5_SHARP, .5)
        await robot.play_note(Note.A5, .5)
        await robot.play_note(Note.D6, .5)
        HAS_SWEPT = True
    else:
        if dist <= 10:
            await robot.set_wheel_speeds(0,0)
            if ROTATION_DIR == "clockwise":
                await robot.turn_right(90)
                ROTATION_DIR = "counter-clockwise"
            else:
                await robot.turn_left(90)
                ROTATION_DIR = "clockwise"
            readings = (await robot.get_ir_proximity()).sensors
            middle = readings[3]
            dist = 4095 / (middle + 1)
            if dist <  ROBOT_MOVE_DISTANCE:
                await robot.move((1/3) * dist)
            else:
                await robot.move(ROBOT_MOVE_DISTANCE)
            if ROTATION_DIR == "clockwise":
                await robot.turn_left(90)
            else:
                await robot.turn_right(90)
        await robot.set_wheel_speeds(SPEED,SPEED)





async def getToOrigin(robot):
    global HAS_COLLIDED, HAS_EXPLORED, HAS_SWEPT, SENSOR2CHECK
    global ROTATION_DIR, CORNERS, DESTINATION, ARRIVAL_THRESHOLD
    global SPEED, ROBOT_MOVE_DISTANCE, AT_ORIGIN
    await robot.set_wheel_speeds(SPEED,SPEED)
    
    current_position = await robot.get_position()
    pos = current_position.x, current_position.y
    readings = (await robot.get_ir_proximity()).sensors
    
    middle = readings[3]
    sidesens = readings[SENSOR2CHECK]
    sidedist = 4095 / (sidesens + 1)
    if sidedist <= 5 or sidedist > 10:
        await robot.set_wheel_speeds(0,0)
        if ROTATION_DIR == "clockwise":
            if sidedist <= 5:
                await robot.turn_right(3)
            if sidedist > 10:
                await robot.turn_left(3)
        else:
            if sidedist <= 5:
                await robot.turn_left(3)
            if sidedist > 10:
                await robot.turn_right(3)
        await robot.set_wheel_speeds(SPEED, SPEED)
    dist = 4095 / (middle + 1)
    if dist < 10:
        await robot.set_wheel_speeds(0,0)
        if ROTATION_DIR == "clockwise":
            await robot.turn_right(90)
        else:
            await robot.turn_left(90)
        await robot.set_wheel_speeds(SPEED,SPEED)
    current_position = await robot.get_position()
    pos = current_position.x, current_position.y
    if checkPositionArrived(pos, (0,0), ARRIVAL_THRESHOLD):
        await robot.set_wheel_speeds(0,0)
        await robot.set_lights_spin_rgb(0, 255, 0)
        await robot.play_note(Note.E5, .2)
        await robot.play_note(Note.E5, .2)
        await robot.play_note(Note.E5, .4)
        await robot.play_note(Note.E5, .2)
        await robot.play_note(Note.E5, .2)
        await robot.play_note(Note.E5, .4)
        await robot.play_note(Note.E5, .2)
        await robot.play_note(Note.G5, .2)
        await robot.play_note(Note.C5, .2)
        await robot.play_note(Note.D5, .2)
        await robot.play_note(Note.E5, .8)
        
        
        
        AT_ORIGIN = True
    





    


# start the robot
robot.play()
