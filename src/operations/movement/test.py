import time

from src.operations.movement.movement import moveForward, stopMoving, turnLeft, stopTurning, turnRight

print("moving forward")
moveForward(1.5)

time.sleep(3)

print("stopping")
stopMoving()
