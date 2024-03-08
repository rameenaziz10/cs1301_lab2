from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())   # Put robot name here.

# IR Sensor Angles
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

# --------------------------------------------------------
# Implement the first two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_touched(robot):
    pass

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    pass

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
    """
    Use the following two lines somewhere in your code to calculate the
    angle and direction of reflection from a list of IR readings:
        (approx_dist, approx_angle) = angleOfClosestWall(ir_readings)
        (direction, turningAngle) = calculateReflectionAngle(approx_angle)
    Then, if the closest wall is less than 20 cm away, use the
    direction and the turningAngle to determine how to rotate the robot to
    reflect.
    """
    pass

def angleOfClosestWall(readings):
    """Remember that this function can be autograded!"""
    IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]

def calculateReflectionAngle(angle):
    """Remember that this function can be autograded!"""
    pass

# start the robot
robot.play()
