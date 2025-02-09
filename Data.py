import SerialReader


class DataManager:
    def __init__(self, reader: SerialReader, parsers: list):

        self.reader = reader
        self.parsers = parsers 

    def process_next_line(self):
        line = self.reader.read_line()
        if line is None:
            return None
        
        for parser in self.parsers:
            parsed_data = parser.parse(line)
            if parsed_data is not None:
                return parsed_data
        
        return None
