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
            serialData = (nodeData, humidityData)
            print(uselessData)
            return serialData

 
        

def nodeNumber(sData:tuple):
    pattern = r'^Node:\s*(\d+)$'
    node = sData[0]    

    match = re.match(pattern, node)
    if match:
        node_value = match.group(1)
        return node_value
    


def main_loop():
    while True:
        data = GetSerial()
        Node = nodeNumber(data)
        print(Node)


if __name__ == "__main__":
    main_loop()
    