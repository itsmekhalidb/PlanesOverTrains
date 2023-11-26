import pandas as pd

class block_info:
    def __init__(self, filepath: str):
        if filepath == "":
            self.block_dict = {}
            self.station_list = {}
            self.switch_list = {"blue" : {"5" : ["6", "11"]},
                "green" : {"1" : "13", "13" : "12", "150" : "28",
                    "28" : "29", "76" : "77", "77" : "101",
                    "85" : "86", "100" : "85"},
                "red" : {"16" : ["1", "15"], "27" : "76",
                    "32" : "72", "38" : "71", "43" : "67",
                    "52" : "66"}}
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
                block_list = []
                beacon = str(block_info['beacon'])
                if beacon.startswith("Station: "):
                    index_of_parenthesis = beacon.find('(')
                    station_name = beacon[9:index_of_parenthesis] if index_of_parenthesis != -1 else beacon[9:]
                    if station_name in line_stations:
                        line_stations[station_name].append(block_number)
                    else:
                        block_list.append(block_number)
                        line_stations[station_name] = block_list  # Include block number along with station name
            output[line] = line_stations
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
        for block_number, block_info in self.block_dict[line].items():
            if block_info['section'] == section:
                blocks.append(str(block_number))
        return blocks
    
    # return switch inputs and their respective outputs
    def get_switch_list(self, line):
        return self.switch_list[line]

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
# red_48 = tm.get_block_info('red', 1)
# print(red_48)
# red_48 = tm.get_block_info('green', 1)
# print(red_48)
# tm = block_info('block_information.xlsx')
# red_sections = tm.get_section_list('green')
# print(red_sections)
# tm = block_info('block_information.xlsx')
# stations = tm.get_station_list()['green']
# for station_name, block_number in stations.items():
#     print(f"{station_name}, {block_number}")
