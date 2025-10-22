
import odrive
from typing import Final



AXIS_STATE_CLOSED_LOOP_CONTROL: Final = 8
IDLE: Final = 1 #helps with motor twitching

odrv0 = odrive.find_any()

odrv0.axis0.controller.input_vel = 1

odrv0.axis1.controller.input_vel = 1