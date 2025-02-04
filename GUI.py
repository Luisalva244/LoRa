import serial
import time


esp32 = serial.Serial(port= '/dev/ttyUSB1', baudrate=115200, timeout=1)

try:
    while True:
        if esp32.in_waiting > 0:  # Check if there's data available to read
            data = esp32.readline().decode('utf-8').strip()  # Read and decode
            print(f"Received: {data}")  # Print received data

except KeyboardInterrupt:
    print("\nClosing connection...")
    esp32.close()