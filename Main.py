from SerialReader import PySerialReader
import time
from Humidity import HumidityParser
from Node import NodeParser
from Data import DataManager
from ExcelWriter import ExcelWriter

def main():
    serial_reader = PySerialReader(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
    
    node_parser = NodeParser()
    humidity_parser = HumidityParser()
    parsers = [node_parser, humidity_parser]

    manager = DataManager(reader=serial_reader, parsers=parsers)
    count = 0
    while True:
        data = manager.process_next_line()
        if data:
            count += 1
            tipo = data['type']
            valor = data['value']
            writeNode = ExcelWriter().writeNode(data, count)
            writeHumidity = ExcelWriter().writeHumidity(data, count)
            print(f"({count}) {tipo}: {valor}")

if __name__ == "__main__":
    main()

