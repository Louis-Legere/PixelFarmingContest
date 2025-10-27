import odrive
import movement
from src.operations.movement.movement import moveForward, stopMoving

odrv0 = odrive.find_any()

#odrv0.axis0.controller.input_vel = 0
#odrv0.axis1.controller.input_vel = 0

stopMoving()


