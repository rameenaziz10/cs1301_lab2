from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
name = "BAYMAX"
robot = Create3(Bluetooth(name))   # Put robot name here.

# --------------------------------------------------------
# Implement the first two functions so that the robot
# will stop and turn on a solid red light
# when any button or bumper is pressed.
# --------------------------------------------------------
buttonpress = False
# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_touched(robot):
    global buttonpress
    buttonpress = True

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global buttonpress
    buttonpress = True


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
    while not buttonpress:
        readings = (await robot.get_ir_proximity()).sensors
        middle = readings[3]
        distance = 4095 / (middle + 1)
        if distance <= 5:
            speed = 0
            color = (255,0,0)
            note = Note.D7
        elif distance <= 30:
            speed = 1
            color = (255,165,0)
            note = Note.D6
        elif distance <= 100:
            speed = 4
            color = (255,255,0)
            note = Note.D5
        elif distance > 100:
            color = (0,255,0)
            speed = 8
            note = ""
        
        red, green, blue = color
        await robot.set_lights_rgb(red, green, blue)
        await robot.set_wheel_speeds(speed,speed)
        if type(note) != str:
            await robot.play_note(note,1)
            
        if buttonpress:
            
            await robot.set_lights_rgb(255,0,0)
            await robot.set_wheel_speeds(0,0)


# start the robot
robot.play()
