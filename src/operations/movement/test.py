import time

from src.operations.movement.movement import moveForward, stopMoving, turnLeft, stopTurning, turnRight

print("moving forward")
moveForward(0.8)

time.sleep(2)

print("stopping")
stopMoving()
