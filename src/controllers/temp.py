import time

from src.controllers import movementController

print("tranisiton to idle")
movementController.set_motor_state_idle()

print("transition to closed loop")
movementController.set_motor_state_closed_loop()

print("tranisiton to idle")
movementController.set_motor_state_idle()

print("transition to closed loop")
movementController.set_motor_state_closed_loop()
