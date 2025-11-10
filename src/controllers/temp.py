import time

from src.controllers import movementController

print("moving forward")
movementController.transferToForward(1.5)

time.sleep(3)

print("turning left")
movementController.transferToLeft(20)

time.sleep(3)

print("moving forward")
movementController.transferToForward(1.5)

time.sleep(3)

print("turning right")
movementController.transferToRight(20)

time.sleep(3)

print("moving forward")
movementController.transferToForward(1.5)

time.sleep(3)

print("moving backwards")
movementController.transferToBackward(1.5)

time.sleep(3)

print("stopping")
movementController.transferToStop()
