
from src.utils.uartConnection import connection
from typing import Final
import time

maxSpeed: Final = 2
accelerationWaitTime = 0.01 #time that a certain speed is being used during acceleration
decelerationWaitTime = 0.01
decelerationSteps = 100

#predefined states
AXIS_STATE_CLOSED_LOOP_CONTROL: Final = 8
IDLE: Final = 1 #helps with motor twitching

# Helper function to send a command via UART
def send_command(command: str):
    """Send a command string to the motor controller via UART."""
    if not connection.is_open:
        raise ConnectionError("UART connection is not open.")
    connection.write((command + "\n").encode("utf-8"))
    time.sleep(0.001)  # small delay to avoid overwhelming the microcontroller

def moveForward(velocity: float):
    steps = int(velocity * 100) + 1  # 1.55 * 100 is 155. +1 = 156

    for i in range(steps): # 0 ... 155
        speed = i / 100  # convert back to float
        send_command(f"v 0 {speed}") # v = velocity; 0 = axisNumber; speed = velocity
        send_command(f"v 1 {speed}")
        print(f"Current speed: {speed}")
        time.sleep(accelerationWaitTime)

def moveBackwards(velocity):
    for i in range(int( abs(velocity) * 100 + 1)):  # in case of velocity = 1.55 its 156. So the loop goes 0,1,2 ... 155. And 155 divided by 100 is 1.55 again
        send_command(f"v 0 {(i / 100) * -1}") #negative cause backwards
        send_command(f"v 1 {(i / 100) * -1}")
        print(f"Current speed: {(i / 100) * -1}")
        time.sleep(accelerationWaitTime)

def stopMoving():
    send_command("f 0")  # axis 0
    response = connection.readline().decode().strip()
    parts = response.split()
    velAxis0 = float(parts[1])

    send_command("f 1")  # axis 1
    response = connection.readline().decode().strip()
    parts = response.split()
    velAxis1 = float(parts[1])

    # Compute decrement per step
    decrementAxis0 = velAxis0 / decelerationSteps
    decrementAxis1 = velAxis1 / decelerationSteps

    for i in range(decelerationSteps):
        # Reduce velocity but do not go below zero
        send_command("f 0")  # axis 0
        response = connection.readline().decode().strip()
        parts = response.split()
        currentVelAxis0 = float(parts[1])

        send_command("f 1")  # axis 1
        response = connection.readline().decode().strip()
        parts = response.split()
        currentVelAxis1 = float(parts[1])

        send_command(f"v 0 {max(0, currentVelAxis0 - decrementAxis0)}")
        send_command(f"v 1 {max(0, currentVelAxis1 - decrementAxis1)}")

        # Print current velocities
        print(f"speed axis0 = {max(0, currentVelAxis0 - decrementAxis0):.2f}")
        print(f"speed axis1 = {max(0, currentVelAxis1 - decrementAxis1):.2f}")
        time.sleep(decelerationWaitTime)

    # Ensure velocities are exactly zero at the end
    send_command(f"v 0 0")
    send_command(f"v 1 0")

def turnRight(percentage: float):
    """Make right turn by increasing left wheel speed by a small percentage"""
    pct = percentage / 100  # convert 20 -> 0.2

    # Read current velocities
    send_command("f 0")  # left wheel
    vel_left = float(connection.readline().decode().strip().split()[1])

    send_command("f 1")  # right wheel
    vel_right = float(connection.readline().decode().strip().split()[1])

    # Left wheel spins faster
    new_vel_left = vel_left * (1 + pct)

    send_command(f"v 0 {new_vel_left}")
    # right wheel stays the same
    send_command(f"v 1 {vel_right}")


def turnLeft(percentage: float):
    """Make left turn by increasing right wheel speed by a small percentage"""
    pct = percentage / 100  # convert 20 -> 0.2

    # Read current velocities
    send_command("f 0")  # left wheel
    vel_left = float(connection.readline().decode().strip().split()[1])

    send_command("f 1")  # right wheel
    vel_right = float(connection.readline().decode().strip().split()[1])

    # Right wheel spins faster
    new_vel_right = vel_right * (1 + pct)

    send_command(f"v 1 {new_vel_right}")
    # left wheel stays the same
    send_command(f"v 0 {vel_left}")


def stopTurning():
    send_command("f 0")  # axis 0
    response = connection.readline().decode().strip()
    parts = response.split()
    currentVelAxis0 = float(parts[1])

    send_command("f 1")  # axis 1
    response = connection.readline().decode().strip()
    parts = response.split()
    currentVelAxis1 = float(parts[1])

    if currentVelAxis0 < currentVelAxis1:
        send_command(f"v 1 {currentVelAxis0}")
    else:
        send_command(f"v 0 {currentVelAxis1}")

def turnBy90DegreesRight(): #right wheel does not move
    return

def turnBy90DegreesLeft(): #left wheel does not move
    return



