
import odrive
from typing import Final
import time



AXIS_STATE_CLOSED_LOOP_CONTROL: Final = 8
IDLE: Final = 1 #helps with motor twitching


odrv0 = odrive.find_any()
time.sleep(3)

for i in range(11):  # 0,1,2,3,4,5,6,7,8,9,10
    odrv0.axis0.controller.input_vel = i / 10
    odrv0.axis1.controller.input_vel = i / 10
    time.sleep(1)