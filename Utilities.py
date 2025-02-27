import re

class soilHumidityParser:
## Parse the humidity level of the node
    def __init__(self):
        self.regex = re.compile(r'^soilHumidity:\s*(\d+(\.\d+)?)$')

    def parse(self, line: str):
        match = self.regex.match(line)
        if match:
            return {'type': 'soilHumidity','value': float(match.group(1))}
        return None



class HumidityParser:
## Parse the humidity level of the node
    def __init__(self):
        self.regex = re.compile(r'^Humidity:\s*(\d+(\.\d+)?)$')

    def parse(self, line: str):
        match = self.regex.match(line)
        if match:
            return {'type': 'humidity','value': float(match.group(1))}
        return None
    

class TemperatureParser:
## Parse the temperature of the node
    def __init__(self):
        self.regex = re.compile(r'^Temperature:\s*(\d+(\.\d+)?)$')

    def parse(self, line: str):
        match = self.regex.match(line)
        if match:
            return {'type': 'temperature','value': float(match.group(1))}
        return None


class NodeParser:
## This class parse the node that is sending the information

    def __init__(self):
        self.regex = re.compile(r'^Node:\s*(\d+)$')

    def parse(self, line: str):
        match = self.regex.match(line)
        if match:
            return {'type': 'node','value': int(match.group(1))}
        return None