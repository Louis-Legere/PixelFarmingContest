
import odrive
from typing import Final
import time

maxSpeed: Final = 2
accelerationWaitTime = 0.01 #time that a certain speed is being used during acceleration
decelerationWaitTime = 0.01
decelerationSteps = 100

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

def moveBackwards(velocity):
    for i in range(int( abs(velocity) * 100 + 1)):  # in case of velocity = 1.55 its 156. So the loop goes 0,1,2 ... 155. And 155 divided by 100 is 1.55 again
        odrv0.axis0.controller.input_vel = (i / 100) * -1 #negative cause backwards
        odrv0.axis1.controller.input_vel = (i / 100) * -1
        print((i / 100) * -1)
        time.sleep(accelerationWaitTime)

def stopMoving():
    # Read current velocities
    currentVelAxis0 = odrv0.axis0.controller.input_vel
    currentVelAxis1 = odrv0.axis1.controller.input_vel

    # Compute decrement per step
    decrementAxis0 = currentVelAxis0 / decelerationSteps
    decrementAxis1 = currentVelAxis1 / decelerationSteps

    for i in range(decelerationSteps):
        # Reduce velocity but do not go below zero
        odrv0.axis0.controller.input_vel = max(0, odrv0.axis0.controller.input_vel - decrementAxis0)
        odrv0.axis1.controller.input_vel = max(0, odrv0.axis1.controller.input_vel - decrementAxis1)

        # Print current velocities
        print(f"speed axis0 = {odrv0.axis0.controller.input_vel:.2f}")
        print(f"speed axis1 = {odrv0.axis1.controller.input_vel:.2f}")

        time.sleep(decelerationWaitTime)

    # Ensure velocities are exactly zero at the end
    odrv0.axis0.controller.input_vel = 0
    odrv0.axis1.controller.input_vel = 0

def turnLeft(velocity): #turns left with the right wheels velocity left wheel also spins slowly
    return

def turnRight(velocity): #turns right with the left wheels velocity right wheel also spinns slowly
    return

def turnBy90DegreesRight(): #right wheel does not move
    return

def turnBy90DegreesLeft(): #left wheel does not move
    return



