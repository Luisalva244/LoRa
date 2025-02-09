import re

class NodeParser:
## This class parse the node that is sending the information

    def __init__(self):
        self.regex = re.compile(r'^Node:\s*(\d+)$')

    def parse(self, line: str):
        match = self.regex.match(line)
        if match:
            return {'type': 'node','value': int(match.group(1))}
        return None