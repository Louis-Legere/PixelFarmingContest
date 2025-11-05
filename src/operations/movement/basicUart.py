import serial
import time

# Replace with your Jetson's UART port connected to ODrive
uart_port = "/dev/ttyTHS1"
baud_rate = 115200

ser = serial.Serial(uart_port, baud_rate, timeout=1)

def set_motor_velocity(velocity):
    # ODrive simple UART command for motor 0 and 1 velocity
    cmd_motor0 = f"v 0 {velocity}\n"
    cmd_motor1 = f"v 1 {velocity}\n"

    ser.write(cmd_motor0.encode())
    time.sleep(0.05)
    ser.write(cmd_motor1.encode())
    time.sleep(0.05)

    # Optional: read responses
    resp0 = ser.readline().decode().strip()
    resp1 = ser.readline().decode().strip()
    print("Motor 0:", resp0)
    print("Motor 1:", resp1)

try:
    set_motor_velocity(1)
    print("Motors set to velocity 1")
finally:
    ser.close()
