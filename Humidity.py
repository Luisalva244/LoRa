import re

class HumidityParser:
## Parse the humidity level of the node
    def __init__(self):
        self.regex = re.compile(r'^Humidity:\s*(\d+(\.\d+)?)$')

    def parse(self, line: str):
        match = self.regex.match(line)
        if match:
            return {'type': 'humidity','value': float(match.group(1))}
        return None
