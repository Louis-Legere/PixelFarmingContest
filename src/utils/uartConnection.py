import serial

uart_port = "/dev/ttyTHS1"
baud_rate = 115200

try:
    connection = serial.Serial(uart_port, baud_rate, timeout=1)
    print(f"Connected to {uart_port} at {baud_rate} baud.")
except serial.SerialException as e:
    raise ConnectionError(f"Failed to open serial port {uart_port}: {e}")
