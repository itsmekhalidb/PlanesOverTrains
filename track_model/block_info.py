import pandas as pd

class block_info:
    def __init__(self, filepath: str):
        if filepath == "":
            self.block_dict = {}
            self.station_list = {}
            # 1 indicates blocks after count up, 0 indicates count down
            # block 0 is yard
            # self.switch_list = {"blue" : {"5" : [["6", "11"], [0, 1, 1]]},
            #     "green" : {"13" : [["1", "12"], [1, 1, 0]],
            #         "28" : [["29", "150"], [0, 1, -1]],
            #         "57" : [["0", "58"], [-1, 1, 1]],
            #         "63" : [["62","0"], [1, -1, -1]],
            #         "77" : [["101","76"], [1, 1, -1]],
            #         "85" : [["86","100"], [0, 1, -1]]},
            #     "red" : {"9" : [["0", "10"], [0, 1, 1]],
            #         "16" : [["1", "15"], [1, 1, 0]],
            #         "27" : [["28", "76"], [0, 1, 0]],
            #         "33" : [["72", "32"], [1, 1, 0]],
            #         "38" : [["39", "71"], [0, 1, 0]],
            #         "44" : [["67", "43"], [1, 1, 0]],
            #         "52" : [["53", "66"], [0, 1, 0]]}}
            self.switch_list = {
                "blue" : 
                    {"5" : {"6" : 1, "11" : 1}},
                "green" :
                    {"0" : {"63" : 1},
                    "1" : {"13" : 1},
                    "13" : {"1" : 1, "12" : 0},
                    "28" : {"29" : 1},
                    "57" : {"0" : 1, "58" : 1},
                    "62" : {"63" : 1},
                    "76" : {"77" : 1},
                    "77" : {"101" : 1},
                    "85" : {"86" : 1},
                    "100" : {"85" : 0},
                    "150" : {"28" : 0}},
                "red" : 
                    {"0" : {"9" : 0},
                    "1" : {"16" : 1},
                    "9" : {"10" : 1},
                    "10" : {"9" : 0},
                    "27" : {"28" : 1, "76" : 0},
                    "28" : {"27" : 0},
                    "32" : {"33" : 1},
                    "33" : {"32" : 0, "72" : 1},
                    "38" : {"39" : 1, "71" : 0},
                    "43" : {"44" : 1},
                    "44" : {"43" : 0, "67" : 1},
                    "52" : {"53" : 1, "66" : 0},
                    "53" : {"52" : 0},
                    "66" : {"52" : 0},
                    "76" : {"27" : 0}}
            }
            self.light_list = {"blue" : ["5", "6", "11"],
                "green" : ["1", "13", "28", "62", "76", "77", "85", "100", "150"],
                "red" : ["1", "9", "10", "15", "16", "27", "28", "32", "33", "38",
                    "39", "43", "44", "52", "53", "66", "67", "71", "72", "76"]}
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

    def get_light_list(self, line):
        return self.light_list[line]

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
