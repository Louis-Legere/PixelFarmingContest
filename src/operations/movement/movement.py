from src.utils.uartConnection import connection
from typing import Final
import time

# Constants
maxSpeed: Final = 2
accelerationWaitTime = 0.01
decelerationWaitTime = 0.01
decelerationSteps = 100

# Keep track of current velocities in Python
current_velocity = {"0": 0.0, "1": 0.0}  # axis0 = left, axis1 = right

# Helper function to send a command via UART
def send_command(command: str):
    if not connection.is_open:
        raise ConnectionError("UART connection is not open.")
    connection.write((command + "\n").encode("utf-8"))
    time.sleep(0.001)  # small delay to avoid overwhelming the microcontroller

# Forward / Backward
def moveForward(velocity: float):
    steps = int(velocity * 100) + 1
    for i in range(steps):
        speed = i / 100
        current_velocity["0"] = speed
        current_velocity["1"] = speed
        send_command(f"v 0 {speed}")
        send_command(f"v 1 {speed}")
        print(f"Current speed: {speed:.2f}")
        time.sleep(accelerationWaitTime)

def moveBackwards(velocity: float):
    steps = int(abs(velocity) * 100) + 1
    for i in range(steps):
        speed = -(i / 100)
        current_velocity["0"] = speed
        current_velocity["1"] = speed
        send_command(f"v 0 {speed}")
        send_command(f"v 1 {speed}")
        print(f"Current speed: {speed:.2f}")
        time.sleep(accelerationWaitTime)

# Stop
def stopMoving():
    vel0 = current_velocity["0"]
    vel1 = current_velocity["1"]

    dec0 = vel0 / decelerationSteps
    dec1 = vel1 / decelerationSteps

    for _ in range(decelerationSteps):
        vel0 = max(0, vel0 - dec0) if vel0 > 0 else min(0, vel0 - dec0)
        vel1 = max(0, vel1 - dec1) if vel1 > 0 else min(0, vel1 - dec1)
        current_velocity["0"] = vel0
        current_velocity["1"] = vel1
        send_command(f"v 0 {vel0}")
        send_command(f"v 1 {vel1}")
        print(f"speed axis0 = {vel0:.2f}, axis1 = {vel1:.2f}")
        time.sleep(decelerationWaitTime)

    current_velocity["0"] = 0.0
    current_velocity["1"] = 0.0
    send_command("v 0 0")
    send_command("v 1 0")

# Turning
def turnLeft(percentage: float):
    pct = percentage / 100
    current_velocity["1"] = current_velocity["1"] * (1 + pct)
    send_command(f"v 1 {current_velocity['1']}")
    print(f"Turning left: left={current_velocity['0']:.2f}, right={current_velocity['1']:.2f}")

def turnRight(percentage: float):
    pct = percentage / 100
    current_velocity["0"] = current_velocity["0"] * (1 + pct)
    send_command(f"v 0 {current_velocity['0']}")
    print(f"Turning right: left={current_velocity['0']:.2f}, right={current_velocity['1']:.2f}")

def stopTurning():
    slower = min(current_velocity["0"], current_velocity["1"])
    current_velocity["0"] = slower
    current_velocity["1"] = slower
    send_command(f"v 0 {slower}")
    send_command(f"v 1 {slower}")
    print(f"Stopping turn: axis0 = {slower:.2f}, axis1 = {slower:.2f}")

# 90-degree turns (to be implemented)
def turnBy90DegreesRight():
    pass

def turnBy90DegreesLeft():
    pass
