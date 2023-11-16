import pandas as pd

class block_info:
    def __init__(self, filepath: str):
        if filepath == "":
            self.block_dict = {}
            self.station_list = {}
        else:
            print("Loading block info from " + filepath)
            self.block_dict = self.load_block_info(filepath)

    def load_block_info(self, filepath: str):
        df = pd.read_excel(filepath)
        block_dict = {}

        for index, row in df.iterrows():
            line = row['line color'].lower()
            block_number = row['block number']

            block_info = {
                'grade': row['grade'],
                'elevation': row['elevation'],
                'length': row['length'],
                'section': row['section'],
                'speed limit': row['speed limit'],
                'switch position': bool(row['switch position']),
                'underground': bool(row['underground']),
                'beacon': row['beacon'],
                'station side': row['station side']
            }

            if line in block_dict:
                block_dict[line][block_number] = block_info
            else:
                block_dict[line] = {block_number: block_info}


        return block_dict

    # return stations on each line and their blocks
    def get_station_list(self):
        output = {}
        for line in self.block_dict:
            line_stations = {}
            for block_number, block_info in self.block_dict[line].items():
                beacon = str(block_info['beacon'])
                if beacon.startswith("Station: "):
                    index_of_parenthesis = beacon.find('(')
                    station_name = beacon[9:index_of_parenthesis] if index_of_parenthesis != -1 else beacon[9:]
                    line_stations[station_name] = block_info
            output[line] = line_stations.keys()
        return output

    # return sections in a line
    def get_section_list(self, line):
        line_sections = set()  # Use a set to automatically handle uniqueness
        if line in self.block_dict:
            for block_number, block_info in self.block_dict[line].items():
                if block_info['section'] not in line_sections:
                    line_sections.add(block_info['section'])
        return list(line_sections)

    # return blocks in a section
    def get_block_list(self, line, section):
        blocks = []
        for block in self.block_dict[line]:
            if block['section'] == section:
                blocks.append(block['block_number'])
        return blocks

    def get_block_info(self, line, block_number):
        if line in self.block_dict and block_number in self.block_dict[line]:
            return self.block_dict[line][block_number]
        else:
            # print("Block " + str(block_number) + " on line " + line + " not found")
            return None

    def get_all_blocks_for_line(self, line):
        return self.block_dict.get(line.lower(), {})

    def __str__(self):
        return str(self.block_dict)

# How to Use:
# tm = block_info('block_information.xlsx')
# red_48 = tm.get_block_info('red', 1)['length']
# print(red_48)
# tm = block_info('block_information.xlsx')
# red_sections = tm.get_section_list('green')
# print(red_sections)
# tm = block_info('block_information.xlsx')
# stations = list(tm.get_station_list()['green'])
# print(stations)