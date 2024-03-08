from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

robot = Create3(Bluetooth())   # Put robot name here.

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
# Implement avoidCollision() so that the robot CONTINUOUSLY 
# reads the IR measurement from the CENTER sensor.
# When the robot senses that the wall in front of the robot is:
#     <= 5 units away, stop the robot, set a red light, and play D7.
#     <= 30 units away, slow down the robot to 1 unit/s, set an orange light,
#        and play D6.
#     <= 100 units away, move the robot at a moderate speed (4 units/s), 
#        set a yellow light, and play D5.
#     > 100 units away, proceed at a faster pace (8 units/s), set a green light.
# --------------------------------------------------------

@event(robot.when_play)
async def avoidCollision(robot):
    pass

# start the robot
robot.play()
