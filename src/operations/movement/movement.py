
import odrive
from typing import Final
import time

maxSpeed: Final = 2
accelerationWaitTime = 0.01 #time that a certain speed is being used during acceleration

#predefined states
AXIS_STATE_CLOSED_LOOP_CONTROL: Final = 8
IDLE: Final = 1 #helps with motor twitching


odrv0 = odrive.find_any()
time.sleep(1)



def moveForward(velocity): #maximum 2 numbers after the comma
    for i in range(int(velocity * 100 + 1)):  #in case of velocity = 1.55 its 156. So the loop goes 0,1,2 ... 155. And 155 divided by 100 is 1.55 again
        odrv0.axis0.controller.input_vel = i / 100
        odrv0.axis1.controller.input_vel = i / 100
        print(i / 100)
        time.sleep(accelerationWaitTime)


