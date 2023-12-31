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
        self._lights = {'1': 0, '13': 0, '29': 0, '150': 0}
        # 1 = left, 0 = right
        self._switches = {'13': 0, '29': 0, '57': 0, '63': 0, '76': 0, '85': 0}
        # crossing lights/gate
        self._crossing_lights_gates = {'18': 0}
        # if program is in automatic mode
        self._automatic = False
        # commanded speed is speed limit - occupancy
        self._command_speed = {}
        # dict of wayside controllers and their associated PLC files
        self._plc_input = {'Green 1': "", 'Green 2': "", 'Red 1': "", 'Red 2': ""}
        # time to be displayed on the clock
        self._time = 0
        # startup
        self._startup = 0
        # filepath
        self._filepath = ""

        # api signals
        self.ctc_ctrl_signals = ctcsignals
        self.track_ctrl_signals = tracksignals

        try:
            self.update()
        except Exception as e:
            print("track_controller.py not updating")

    def update(self, thread=True):
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

    def get_occupancy(self, block) -> bool:
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


    def get_switch_list(self) -> dict:
        return self._switches

    def get_switch(self, switch):
        return self._switches[switch]

    def set_switch(self, switch, value: int):
        try:
            self._switches[switch] = value
            self.ctc_ctrl_signals._switch[switch] = value
            self.track_ctrl_signals._switches[switch] = value
        except Exception as e:
            print("Invalid switch")

    def get_light(self, light: str) -> int:
        return self._lights[light]

    def get_lights(self) -> list:
        return  self._lights

    def set_lights(self, light: str, value: int):
        try:
            self._lights[light] = value
            self.ctc_ctrl_signals._light[light] = value
            self.track_ctrl_signals._lights[light] = value
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
    # def set_authority(self, _authority: int):
    #     self._authority = _authority
    #
    # def get_authority(self, train: int) -> int:
    #     return self._train_info[train][1]

    def set_suggested_speed(self, _suggested_speed: int, train: int):
        self._train_info[train][2] = _suggested_speed

    def get_suggested_speed(self, train: int) -> float:
        return self._suggested_speed[train][2]

    def set_railway_crossing(self, crossing, _crossing_lights_gates: int):
        self._crossing_lights_gates[crossing] = _crossing_lights_gates
        self.track_ctrl_signals._railway_crossing[crossing] = _crossing_lights_gates

    def get_railway_crossing(self, crossing):
        return self._crossing_lights_gates[crossing]

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
