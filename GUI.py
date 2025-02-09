import serial
import time
import re



esp32 = serial.Serial(port= '/dev/ttyUSB0', baudrate=115200, timeout=1)

def GetSerial():
    while True:
        if esp32.in_waiting > 0:  # Check if there's data available to read
            uselessData = esp32.readline().decode('utf-8').strip()  # Read and decode
            nodeData = esp32.readline().decode('utf-8').strip() 
            humidityData = esp32.readline().decode('utf-8').strip() 
            print(uselessData)
            return nodeData + humidityData


        

def nodeNumber(sData):
    pattern = r'^Node:\s*(\d+)$'
    
    match = re.match(pattern, sData)
    if match:
        node_value = match.group(1)
        return node_value
    
def main_loop():
    while True:
        Node = nodeNumber(GetSerial())
        print(Node)


if __name__ == "__main__":
    main_loop()
    