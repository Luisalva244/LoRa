import serial
import time
import re


class PySerialReader():
    
    #Read serial data and return it 
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        print(f"[INFO] Conectado a {port} a {baudrate} baudios.")

    def read_line(self) -> str:
        if self.ser.in_waiting > 0:
            data = self.ser.readline()
            if data:
                return data.decode('utf-8', errors='replace').strip()
        return None

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("[INFO] Puerto serial cerrado.")
