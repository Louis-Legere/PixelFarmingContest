
from typing import Final
import time
from src.utils import uartConnection
from src.operations.movement import movement

#Remember! Always try to decelerate (stopMoving) first to prevent mechanical stress
# or abrupt torque cutoff on the motors.

# import movement and call functions

#Remember! Change state to idle in odrive, or call set state idle to test if closed loop works 
#predefined states

from enum import Enum, auto

class DrivingState(Enum):
    FORWARD = auto()
    BACKWARD = auto()
    STOP = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()

currentDrivingState = DrivingState.STOP

AXIS_STATE_CLOSED_LOOP_CONTROL: Final = 8
IDLE: Final = 1 #helps with motor twitching

ser = uartConnection.connection

# set the state from idle to closed loop
def set_motor_state_closed_loop():

    # check the current state should be closed loop or 8
    ser.write("r axis0.current_state\n".encode())
    resp0 = ser.readline().decode().strip()

    ser.write("r axis1.current_state\n".encode())
    resp1 = ser.readline().decode().strip()

    ser.write("w axis0.requested_state 8\n".encode())
    ser.write("w axis1.requested_state 8\n".encode())
    time.sleep(0.5) # might need time to enter closed loop

    # check the current state and if it worked
    ser.write("r axis0.current_state\n".encode())
    resp0 = ser.readline().decode().strip()

    ser.write("r axis1.current_state\n".encode())
    resp1 = ser.readline().decode().strip()

    print("Motor 0:", resp0)
    print("Motor 1:", resp1)


# shutting down should go back into Idle
def set_motor_state_idle():

    # check the current state should be idle or 1
    ser.write("r axis0.current_state\n".encode())
    resp0 = ser.readline().decode().strip()

    ser.write("r axis1.current_state\n".encode())
    resp1 = ser.readline().decode().strip()

    ser.write("w axis0.requested_state 1\n".encode())
    ser.write("w axis1.requested_state 1\n".encode())
    time.sleep(0.5) # might need time to enter idle 

    # check the current state and if it worked
    ser.write("r axis0.current_state\n".encode())
    resp0 = ser.readline().decode().strip()

    ser.write("r axis1.current_state\n".encode())
    resp1 = ser.readline().decode().strip()

    print("Motor 0:", resp0)
    print("Motor 1:", resp1)


#higher level api functions that call lower level motor control functions
def transferToForward(velocity):
    global currentDrivingState
    match currentDrivingState:
        case DrivingState.STOP:
            movement.moveForward(velocity)
        case DrivingState.FORWARD:
            pass
        case DrivingState.BACKWARD:
            movement.stopMoving()
            time.sleep(0.5)
            movement.moveForward(velocity)
        case DrivingState.TURN_LEFT:
            movement.stopTurning()
            movement.moveForward(velocity)
        case DrivingState.TURN_RIGHT:
            movement.stopTurning()
            movement.moveForward(velocity)

    currentDrivingState = DrivingState.FORWARD

def transferToBackward(velocity):
    global currentDrivingState
    match currentDrivingState:
        case DrivingState.STOP:
            movement.moveBackwards(velocity)
        case DrivingState.FORWARD:
            movement.stopMoving()
            time.sleep(0.5)
            movement.moveBackwards(velocity)
        case DrivingState.BACKWARD:
            pass
        case DrivingState.TURN_LEFT:
            movement.stopTurning()
            movement.moveBackwards(velocity)
        case DrivingState.TURN_RIGHT:
            movement.stopTurning()
            movement.moveBackwards(velocity)

    currentDrivingState = DrivingState.BACKWARD

def transferToLeft(percentage):
    global currentDrivingState
    match currentDrivingState:
        case DrivingState.STOP:
            movement.turnLeft(percentage)
        case DrivingState.FORWARD:
            movement.turnLeft(percentage)
        case DrivingState.BACKWARD:
            pass #robot cant turn while driving backwards
        case DrivingState.TURN_LEFT:
            pass
        case DrivingState.TURN_RIGHT:
            movement.stopTurning()
            movement.turnLeft(percentage)

    currentDrivingState = DrivingState.TURN_LEFT

def transferToRight(percentage):
    global currentDrivingState
    match currentDrivingState:
        case DrivingState.STOP:
            movement.turnRight(percentage)
        case DrivingState.FORWARD:
            movement.turnRight(percentage)
        case DrivingState.BACKWARD:
            pass #robot cant turn while driving backwards
        case DrivingState.TURN_LEFT:
            movement.stopTurning()
            movement.turnRight(percentage)
        case DrivingState.TURN_RIGHT:
            pass

    currentDrivingState = DrivingState.TURN_RIGHT

def transferToStop():
    global currentDrivingState
    match currentDrivingState:
        case DrivingState.STOP:
            pass
        case DrivingState.FORWARD:
            movement.stopMoving()
        case DrivingState.BACKWARD:
            movement.stopMoving()
        case DrivingState.TURN_LEFT:
            movement.stopMoving()
        case DrivingState.TURN_RIGHT:
            movement.stopMoving()

    currentDrivingState = DrivingState.STOP