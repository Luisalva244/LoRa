from SerialReader import PySerialReader
import time
from Humidity import HumidityParser
from Node import NodeParser
from Data import DataManager
from db import Database


def main():
    node_val = None
    humidity_val = None

    db = Database()

    serial_reader = PySerialReader(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
    
    node_parser = NodeParser()
    humidity_parser = HumidityParser()
    parsers = [node_parser, humidity_parser]

    manager = DataManager(reader=serial_reader, parsers=parsers)

    while True:
        data = manager.process_next_line()

        if data is not None:
            tipo = data['type']      # 'node' o 'humidity'
            valor = data['value']    # número

            if tipo == 'node':
                node_val = valor
            elif tipo == 'humidity':
                humidity_val = valor

            if node_val is not None and humidity_val is not None:
                dbInfo = {
                    'node': node_val,
                    'humidity': humidity_val
                }
                db.writeData(dbInfo)
                print("[INFO] Guardado:", dbInfo)
                
                node_val = None
                humidity_val = None

        time.sleep(0.02)

if __name__ == "__main__":
    main()

