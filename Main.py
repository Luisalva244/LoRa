from SerialReader import PySerialReader
import time
from Humidity import HumidityParser
from Node import NodeParser
from Data import DataManager

def main():
    serial_reader = PySerialReader(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
    
    node_parser = NodeParser()
    humidity_parser = HumidityParser()
    parsers = [node_parser, humidity_parser]

    manager = DataManager(reader=serial_reader, parsers=parsers)
    
    try:
        while True:
            data = manager.process_next_line()
            if data:
                tipo = data['type']
                valor = data['value']
                print(f"{tipo.capitalize()}: {valor}")
            
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("[INFO] Interrupción por teclado. Saliendo...")
    finally:
        serial_reader.close()

if __name__ == "__main__":
    main()

