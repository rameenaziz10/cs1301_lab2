from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
import math as m

robot = Create3(Bluetooth())   # Put robot name here.

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

# --------------------------------------------------------
# Implement these three helper functions so that they
# can be used later on.
# --------------------------------------------------------

# Helper Function 1
def farthestDistance(currPosition, positions):
    """Remember that this function can be autograded!"""
    pass

# Helper Function 2
def movementDirection(readings):
    """Remember that this function can be autograded!"""
    pass

# Helper Function 3
def checkPositionArrived(current_position, destination, threshold):
    """Remember that this function can be autograded!"""
    pass

# --------------------------------------------------------
# Implement the these two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    pass

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    pass

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
    pass


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
    pass



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
    pass

# start the robot
robot.play()
