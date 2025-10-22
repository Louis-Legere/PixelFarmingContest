
import odrive
from typing import Final



AXIS_STATE_CLOSED_LOOP_CONTROL: Final = 8

odrv0 = odrive.find_any()

odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.input_vel = 0

odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.controller.input_vel = 0