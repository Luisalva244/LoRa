from SerialReader import PySerialReader
import time
from Utilities import HumidityParser, soilHumidityParser, NodeParser, TemperatureParser
from Data import DataManager
from db import Database


def main():
    node_val = None
    humidity_val = None
    soil_humidity_val = None
    temperature_val = None

    db = Database()

    serial_reader = PySerialReader(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
    
    node_parser = NodeParser()
    humidity_parser = HumidityParser()
    soil_humidity_parser = soilHumidityParser()
    temperature_parser = TemperatureParser()
    parsers = [node_parser, humidity_parser, soil_humidity_parser, temperature_parser]

    manager = DataManager(reader=serial_reader, parsers=parsers)

    while True:
        data = manager.process_next_line()

        if data is not None:
            tipo = data['type']      
            valor = data['value'] 

            if tipo == 'node':
                node_val = valor
            elif tipo == 'soilHumidity':
                soil_humidity_val = valor
            elif tipo == 'humidity':
                humidity_val = valor
            elif tipo == 'temperature':
                temperature_val = valor

            if node_val is not None and soil_humidity_val is not None and humidity_val is not None and temperature_val is not None:
                dbInfo = {
                    'node': node_val,
                    'soilHumidity': soil_humidity_val,
                    'humidity': humidity_val,
                    'temperature': temperature_val
                }
                db.writeData(dbInfo)
                print("[INFO] Guardado:", dbInfo)
                
                node_val = None
                humidity_val = None

        time.sleep(0.02)

if __name__ == "__main__":
    main()

