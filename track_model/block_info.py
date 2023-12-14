import pandas as pd


class block_info:
    def __init__(self, filepath: str):
        if filepath == "":
            self.filepath = ""
            self.block_dict = {}
            self.station_list = {}
            self.switch_list = {}
            self.light_list = {}
            self.switchionary = {}
        else:
            self.filepath = filepath
            print("Loading block info from " + filepath)
            self.block_dict = self.load_block_info(filepath)

    def load_block_info(self, filepath: str):
        # 1 indicates blocks after count up, 0 indicates count down
        # block 0 is yard

        #current block: [next block, incoming direction, outgoing direction, switch position required (0 or 1), switch position label]
        self.switchionary = {
            "green": {
                1 : [13, -1, 1, 0, "13"],
                13: [12, -1, -1, 1, "13"],
                28: [29, 1, 1, 1, "28"],
                57: [58, 1, 1, 0, "57"], #if switch position is 1, go back to yard
                62: [63, 1, 1, 0, "63"],
                76: [77, 1, 1, 0, "77"],
                77: [101, -1, 1, 1, "77"],
                85: [86, 1, 1, 1, "85"],
                100: [85, 1, -1, 0, "85"],
                150: [28, 1, -1, 0, "28"]
            },
            # TODO: Check to see if there are any missing current block -> next block pairs
            "red": {
                9 : [10, -1, -1, 0, "9"], #if switch position is 1, go back to yard
                15: [16, 1, 1, 0, "16"],
                16: [1, -1, 1, 1, "16"],
                 1: [16, -1, 1, 1, "16"],
                27: [28, 1, 1, 1, "27"],
                32: [33, 1, 1, 0, "33"],
                33: [72, -1, 1, 1, "33"],
                38: [39, 1, 1, 1, "38"],
                43: [44, 1, 1, 0, "44"],
                44: [67, -1, 1, 1, "44"],
                52: [53, 1, 1, 1, "52"],
                66: [52, 1, -1, 0, "52"],
                76: [27, 1, -1, 0, "27"],
                71: [38, 1, -1, 0, "38"]
            }
        }

        self.switch_list = {"blue": {"5": [["6", "11"]]},
                            "green": {"13": [["1", "12"]],
                                      "28": [["150", "29"]],
                                      "57": [["58", "0"]],
                                      "63": [["0", "62"]],
                                      "77": [["76", "101"]],
                                      "85": [["100", "86"]]},
                            "red": {"9": [["10", "0"]],
                                    "16": [["15", "1"]],
                                    "27": [["76", "28"]],
                                    "33": [["32", "72"]],
                                    "38": [["71", "39"]],
                                    "44": [["43", "67"]],
                                    "52": [["66", "53"]]}
                            }
        self.khalids_special_switch_list = { # {"line name" : {"entry block" : {"exit block" : [direction out, direction in, switch position]}, "name" : "name of switch"}}
            #1 is forward 0 is backward
            #to go from here to there, you will be moving in this direction, you must enter from this direction, name of switch
            "blue" :
                {"5" : {"6" : 1, "11" : 1}},
            "green" :
                {"0" : {"63" : [1, 1, 1], "name" : "63"},
                "1" : {"13" : [1, 0, 0], "name" : "13"},
                "13" : {"12" : [0, 0, 1], "name" : "13"},
                "28" : {"29" : [1, 1, 1], "name" : "28"},
                "57" : {"0" : [1, 1, 1], "name" : "57"},
                "76" : {"77" : [1, 1, 0], "name" : "77"},
                "77" : {"101" : [1, 0, 1], "name" : "77"},
                "85" : {"86" : [1, 1, 1], "name" : "85"},
                "100" : {"85" : [0, 1, 0], "name" : "85"},
                "150" : {"28" : [0, 1, 0], "name" : "28"}},
            "red" :
                {"0" : {"9" : [0, 1, 1], "name" : "9"},
                "1" : {"16" : [1, 0, 1], "name" : "16"},
                "9" : {"0" : [0, 1, 1], "name" : "9"},
                "15" : {"16" : [1, 1, 0], "name" : "16"},
                "16" : {"1" : [1, 0, 1], "name" : "16"},
                "27" : {"28" : [1, 1, 1],"name" : "27"},
                "32" : {"33" : [1, 1, 0], "name" : "33"},
                "33" : {"32" : [0, 0, 0], "72" : [1, 0, 1], "name" : "33"},
                "38" : {"39" : [1, 1, 1], "name" : "38"},
                "43" : {"44" : [1, 1, 0], "name" : "44"},
                "44" : {"33" : [0, 0, 0], "67" : [1, 0, 1], "name" : "44"},
                "52" : {"53" : [1, 1, 1], "name" : "52"},
                "66" : {"52" : [0, 1, 0], "name" : "52"},
                "71" : {"38" : [0, 1, 0], "name" : "38"},
                "76" : {"27" : [0, 1, 0], "name" : "27"}}
        }
        self.light_list = {"blue": ["5", "6", "11"],
                           "green": ["1", "12", "29", "63", "76", "77", "85", "100", "101", "150"],
                           "red": ["1", "9", "10", "15", "16", "27", "28", "32", "33", "38",
                                   "39", "43", "44", "52", "53", "66", "67", "71", "72", "76"]}
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

    def get_khalids_special_switch_list(self, line):
        return self.khalids_special_switch_list[line]

    def get_load(self):
        return self.loaded

    def get_switchionary(self,line):
        return self.switchionary[line]

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

    def get_filepath(self):
        return self.filepath

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
