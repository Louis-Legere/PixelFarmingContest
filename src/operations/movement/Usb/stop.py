import time

import odrive
import movement
from src.operations.movement.movement import moveForward, stopMoving, turnLeft, stopTurning, turnRight

odrv0 = odrive.find_any()

#odrv0.axis0.controller.input_vel = 0
#odrv0.axis1.controller.input_vel = 0
print("moving forward")
moveForward(1.5)

time.sleep(3)

print("turning left")
turnLeft(20)

time.sleep(3)

print("moving forward")
stopTurning()

time.sleep(3)

print("turning right")
turnRight(20)

time.sleep(3)

print("moving forward")
stopTurning()

time.sleep(3)

print("stopping")
stopMoving()
