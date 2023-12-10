import traceback
import threading
from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.track_controller_track_model_api import TrackControllerTrackModelAPI


class Track_Controller(object):

    def __init__(self, ctcsignals: CTCTrackControllerAPI, tracksignals: TrackControllerTrackModelAPI):
        # track that is currently being observed
        self._track = {}
        # blocks that are currently occupied
        self._occupied_blocks = {"Green": [],
                                 "Red": []}
        # 0 = red, 1 = green
        self._lights = {"Green": {'1': 0, '13': 0, '28': 0, '150': 0, "62": 0, "76": 0, "77": 0, "85": 0,
                                  "100": 0},
                        "Red": {'1': 0, '15': 0, '16': 0, '10': 0, '76': 0, '72': 0, '71': 0,
                                '67': 0, '52': 0, '53': 0, '66': 0}}
        # 1 = left, 0 = right
        self._switches = {"Green": {'13': 0, '28': 0, '57': 0, '63': 0, '77': 0, '85': 0},
                          "Red": {'16': 0, '9': 0, '27': 0, '33': 0, '38': 0, '44': 0, '52': 0}}
        # crossing lights/gate
        self._crossing_lights_gates = {"Green": {'18': 0},
                                       "Red": {'47': 0}}

        # if program is in automatic mode
        self._automatic = False
        # commanded speed is speed limit - occupancy
        self._command_speed = {}
        # dict of wayside controllers and their associated PLC files
        self._plc_input = {'Green 1': "track_controller/PLCgreen1.txt", 'Green 2': "track_controller/PLCgreen2.txt",
                           'Red 1': "track_controller/PLCred1.txt", 'Red 2': "track_controller/PLCred2.txt"}
        # time to be displayed on the clock
        self._time = 0
        # startup
        self._startup = 0
        # which plc actions are being taken
        self._operator = "switch"
        #line for parsing
        self._line = ""

        self._pos = 0

        # api signals
        self.ctc_ctrl_signals = ctcsignals
        self.track_ctrl_signals = tracksignals

        try:
            self.update()
        except Exception as e:
            print("track_controller.py not updating")

    def update(self, thread=True): #def update(self, thread=False):
        self._filepath = self.track_ctrl_signals._filepath
        if self._startup == 0:
            if self._filepath != "":
                self.ctc_ctrl_signals._track_info = self.track_ctrl_signals._track_info
                startup = 1

        try:
            self._occupied_blocks = self.track_ctrl_signals._occupancy
        except Exception as e:
            print("Cannot update occupied blocks")

        # CTC Office Inputs
        try:
            self.set_time(self.ctc_ctrl_signals._time)
        except Exception as e:
            print("Cannot set time")

        try:
            self.set_track_section_status(self.ctc_ctrl_signals._track_section_status)
        except Exception as e:
            print("Cannot update track section status")

        # CTC Office Outputs
        try:
            self.ctc_ctrl_signals._occupancy = self._occupied_blocks
        except Exception as e:
            print("Cannot send block occupancy")

        # Track Model Outputs
        self.track_ctrl_signals._time = self.get_time()

        # Dont touch it just pass it
        try:
            self.track_ctrl_signals._train_ids = self.ctc_ctrl_signals._train_ids
            self.track_ctrl_signals._train_out = self.ctc_ctrl_signals._train_out
            self.ctc_ctrl_signals._train_in = self.track_ctrl_signals._train_in
            self.ctc_ctrl_signals._filepath = self.track_ctrl_signals._filepath
        except Exception as e:
            print("Cannot pass train info")



        if thread:
            threading.Timer(0.1, self.update).start()

    def set_track_section_status(self, blocks):
        for block in blocks["Green"].keys():
            self.set_occupancy("Green", block, blocks["Green"][block])
        for block in blocks["Red"].keys():
            self.set_occupancy("Red", block, blocks["Red"][block])


    def get_track(self) -> dict:
        return self._track

    def set_track(self, track):
        self._track = track

    def get_occupancy(self, line, block):
        return self._occupied_blocks[line].count(block)

    def get_block_occupancy(self, line) -> dict:
        temp = {}
        for x in self._occupied_blocks[line]:
            temp.update({x: self.get_occupancy(line, x)})
        return temp

    # def set_occupied_blocks(self, blocks):
    #     for i in self._occupied_blocks.keys():
    #         self._occupied_blocks[i] = blocks[i]

    def get_occupied_blocks(self, line) -> list:
        return self._occupied_blocks[line]

    def set_occupancy(self, line, block, value: int):
        if value == 1:
            self._occupied_blocks[line].append(block)
        else:
            self._occupied_blocks[line].remove(block)
        self._occupied_blocks[line].sort()

    def get_speed_limit(self, block) -> float:
        return self._track.get_block_info('green', block)['speed limit']


    def get_switch_list(self, line) -> dict:
        return self._switches[line]

    def get_switch(self, line, switch):
        return self._switches[line][switch]

    def set_switch(self, line, switch, value: int):
        try:
            self._switches[line][switch] = value
            self.ctc_ctrl_signals._switch[line][switch] = value
            self.track_ctrl_signals._switches[line][switch] = value
        except Exception as e:
            print("Invalid switch")

    def get_light(self, line, light):
        return self._lights[line][light]

    def get_lights(self, line):
        return  self._lights[line]

    def set_lights(self, line, light: str, value: int):
        try:
            self._lights[line][light] = value
            self.ctc_ctrl_signals._light[line][light] = value
            self.track_ctrl_signals._lights[line][light] = value
        except Exception as e:
            print("Invalid light")

    def get_automatic(self) -> bool:
        return self._automatic

    def set_automatic(self, auto: bool):
        self._automatic = auto

    def get_commanded_speed(self, train: int) -> float:
        return self._command_speed[train]

    def set_commanded_speed(self, speed: float, block: str):
        self._command_speed[block] = speed

    # Testbench
    def set_authority(self, train: int, authority: int):
        self._train_info[train][0] = authority

    def get_authority(self, train: int) -> int:
        return self._train_info[train][0]

    def set_suggested_speed(self, _suggested_speed: int, train: int):
        self._train_info[train][2] = _suggested_speed

    def get_suggested_speed(self, train: int) -> float:
        return self._suggested_speed[train][2]

    def set_railway_crossing(self, line, crossing, _crossing_lights_gates):
        self._crossing_lights_gates[line][crossing] = _crossing_lights_gates
        self.track_ctrl_signals._railway_crossing[crossing] = _crossing_lights_gates

    def get_railway_crossing(self, line, crossing):
        return self._crossing_lights_gates[line][crossing]

    def get_railway_crossings(self, line):
        return self._crossing_lights_gates[line]

    def set_train_info(self, trains):
        self._train_info = trains

    def get_train_info(self) -> dict:
        return self._train_info

    def set_plc_input(self, wayside: str, plc: str):
        self._plc_input[wayside] = plc

    def get_plc_input(self, wayside: str):
        return self._plc_input[wayside]

    def set_time(self, time):
        self._time = time

    def get_time(self):
        return self._time

    def set_train_out(self, trains: dict):
        self._train_info = trains

    def get_train_out(self):
        return self._train_info

    def get_occupied_section(self, line, block):
        occupancy = 0
        if line == 'Green':
            if block == '0':
                return self.get_occupancy(line, 0)
            elif block == '1':
                for i in range(1, 13, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '13':
                for i in range(13, 29, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '18':
                for i in range(17, 19, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '57':
                for i in range(29, 58, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '76':
                for i in range(59, 77, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '77':
                for i in range(77, 86, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '100':
                for i in range(86, 101, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '150':
                for i in range(101, 151, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
        elif line == 'Red':
            if block == '0':
                return self.get_occupancy(line, 0)
            elif block == '1':
                for i in range(1, 10, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '10':
                for i in range(10, 16, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '16' or block == '27':
                for i in range(16, 30, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '33' or block == '38':
                for i in range(30, 35, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '44' or block == '52':
                for i in range(35, 53, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '66':
                for i in range(53, 67, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '71':
                for i in range(67, 72, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy
            elif block == '77':
                for i in range(72, 78, 1):
                    occupancy = occupancy or self.get_occupancy(line, str(i))
                return occupancy


    def parse_expression(self, line, track):
        tokens = line.split(" ")
        result = None
        i = 0

        while i < len(tokens)-1:
            if tokens[i] == "and" or tokens[i] == "or" or tokens[i] == "!":

                if tokens[i] == "and":
                    result = result and bool(self.get_occupied_section(track, tokens[i+1]))
                    i += 1
                elif tokens[i] == "or":
                    result = result or bool(self.get_occupied_section(track, tokens[i+1]))
                    i += 1
                else:
                    result = not bool(self.get_occupied_section(track, tokens[i+1]))
                    i += 1
            elif tokens[i].isdigit():
                result = bool(self.get_occupied_section(track, tokens[i]))
            elif tokens[i] == "(":
                j = i + 1
                temp = ""
                while tokens[j] != ")":
                    temp += tokens[j]
                    temp += " "
                    j += 1
                result = self.parse_expression(temp.strip(), track)
            i += 1

        return result

    def parse(self, line: str, track):
        return self.parse_expression(line, track)

    def demorg(self, line: str, track):
        temp_line = "! ( ! ( " + line + " ) )"
        return self.parse_expression(temp_line, track)

    def get_operator(self):
        return self._operator

    def set_operator(self, operator: str):
        self._operator = operator

    def launch_ui(self):
        print("Launching Track Controller UI")
        try:
            from track_controller.Track_Controller_SW import Ui_TrackController_MainUI
        except:
            print("Can't import UI")
            traceback.print_exc()
        try:
            self._ui = Ui_TrackController_MainUI(self)
        except:
            print("An error occurred:")
            traceback.print_exc()
