import time

from src.operations.movement.movement import moveForward, stopMoving, turnLeft, stopTurning, turnRight
from src.controllers.movementController import set_motor_state_idle, set_motor_state_closed_loop

set_motor_state_closed_loop()

print("moving forward")
moveForward(0.8)

time.sleep(2)

print("stopping")
stopMoving()

set_motor_state_idle()
