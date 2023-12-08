import traceback
import threading
from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.track_controller_track_model_api import TrackControllerTrackModelAPI


class Track_Controller(object):

    def __init__(self, ctcsignals: CTCTrackControllerAPI, tracksignals: TrackControllerTrackModelAPI):
        # track that is currently being observed
        self._track = {}
        # blocks that are currently occupied
        self._occupied_blocks = []
        # 1 = red, 0 = green
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
            self.set_occupied_blocks(self.track_ctrl_signals._train_occupancy)
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
            print(e)

        # CTC Office Outputs
        try:
            self.ctc_ctrl_signals._occupancy = self.get_block_occupancy()
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

    def set_track_section_status(self, blocks: dict):
        for block in blocks:
            self.set_occupancy(block, blocks[block])

    def get_track(self) -> dict:
        return self._track

    def set_track(self, track):
        self._track = track

    def get_occupancy(self, block):
        return self._occupied_blocks.count(block)

    def get_block_occupancy(self) -> dict:
        temp = {}
        for x in self._occupied_blocks:
            temp.update({x: self.get_occupancy(x)})
        return temp

    def set_occupied_blocks(self, blocks: dict):
        self._occupied_blocks = blocks

    def get_occupied_blocks(self) -> list:
        return self._occupied_blocks

    def set_occupancy(self, block, value: int):
        if value == 1:
            self._occupied_blocks.append(block)
        else:
            self._occupied_blocks.remove(block)
        self._occupied_blocks.sort()

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

    def parse_expression(self, line):
        tokens = line.split(" ")
        result = None
        i = 0

        while i < len(tokens)-1:
            if tokens[i] == "and" or tokens[i] == "or" or tokens[i] == "!":
                # print(tokens[i+1])
                if tokens[i] == "and":
                    result = result and bool(self.get_occupancy(tokens[i+1]))
                    i += 1
                elif tokens[i] == "or":
                    result = result or bool(self.get_occupancy(tokens[i+1]))
                    i += 1
                else:
                    result = not bool(self.get_occupancy(tokens[i+1]))
                    i += 1
            elif tokens[i].isdigit():
                result = bool(self.get_occupancy(tokens[i]))
            elif tokens[i] == "(":
                j = i + 1
                temp = ""
                while tokens[j] != ")":
                    temp += tokens[j]
                    temp += " "
                    j += 1
                result = self.parse_expression(temp.strip())
            i += 1

        return result

    def parse(self, line: str):
        self._line = line
        return self.parse_expression(line)

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
