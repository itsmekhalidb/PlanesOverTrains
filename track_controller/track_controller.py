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
        self._lights = {'A1': 0, 'D13': 0, 'F29': 0, 'Z150': 0}
        # 1 = left, 0 = right
        self._switches = {'D13': 0, 'F29': 0, 'I57': 0}
        # crossing lights/gate
        self._crossing_lights_gates = {'E18': 0}
        # if program is in automatic mode
        self._automatic = False
        # commanded speed is speed limit - occupancy
        self._command_speed = 0
        # list of trains and their info
        self._train_info = {}
        # dict of wayside controllers and their associated PLC files
        self._plc_input = {'Green 1': "", 'Green 2': "", 'Red 1': "", 'Red 2': ""}

        # Testbench Variables
        self._authority = 0
        self._suggested_speed = 30
        # self._test_speed_limit = 0
        self._track_status = {}
        self._time = 0

        # api signals
        self.ctc_ctrl_signals = ctcsignals
        self.track_ctrl_signals = tracksignals
        try:
            self.update()
        except Exception as e:
            print("track_controller.py not updating")

    def update(self, thread=True):
        # Track Model Inputs
        self.set_track(self.track_ctrl_signals._green)

        # CTC Office Inputs
        # self.set_authority(self.ctc_ctrl_signals._authority) #TODO need to get from individual Train ID
        self.set_commanded_speed(self.ctc_ctrl_signals._suggested_speed)
        self.set_train_info(self.ctc_ctrl_signals._train_info)
        self.set_time(self.ctc_ctrl_signals._time)
        # self.set_track_section_status(self.ctc_ctrl_signals._track_section_status)

        # CTC Office Outputs
        self.ctc_ctrl_signals._occupancy = self.get_block_occupancy()
        # self.ctc_ctrl_signals._green = self.get_track()

        # Track Model Outputs
        self.track_ctrl_signals._authority = self.get_authority()
        self.track_ctrl_signals._commanded_speed = self.get_commanded_speed()
        # self.track_ctrl_signals._green = self.get_track()
        self.track_ctrl_signals._train_info = self.get_train_info()
        self.track_ctrl_signals._time = self.get_time()

        if thread:
            threading.Timer(0.1, self.update).start()

    def get_track_section_status(self):
        return self._track_status

    def set_track_section_status(self, block):
        self._track_status = block
        for i in block.keys():
            self._track[i][2] = int(block[i])

    def get_track(self) -> dict:
        return self._track

    def set_track(self, track):
        self._track = track

    def get_occupancy(self, block) -> int:
        return self._track[block][2]

    def get_block_occupancy(self) -> dict:
        temp = {}
        for x in self._occupied_blocks:
            temp.update({x: self.get_occupancy(x)})
        return temp

    def get_occupied_blocks(self) -> list:
        temp = []
        for x in self._occupied_blocks:
            temp.append(x + '          ' + str(self._track[x][1]) + ' mph')
        return temp

    def set_occupancy(self, block, value: int):
        self._track[block][2] = value
        self.ctc_ctrl_signals._green[block][2] = value
        if value == 1:
            self._occupied_blocks.append(block)
        else:
            self._occupied_blocks.remove(block)
        self._occupied_blocks.sort()

    def get_speed_limit(self, block) -> float:
        return self._track[block][1]

    def set_speed_limit(self, block, value: float):
        self._track[block][1] = value

    def get_switch_list(self) -> dict:
        return self._switches

    def get_switch(self, switch):
        return self._track[switch][3]

    def set_switch(self, switch, value: int):
        self._switches[switch] = value
        self._track[switch][3] = value
        self.ctc_ctrl_signals._green[switch][3] = value
        self.track_ctrl_signals._green[switch][3] = value

    def get_lights(self, light):
        return  self.ctc_ctrl_signals._green[light][4]

    def set_lights(self, light, value):
        self._track[light][4] = value
        self.ctc_ctrl_signals._green[light][4] = value
        self.track_ctrl_signals._green[light][4] = value

    def get_automatic(self) -> bool:
        return self._automatic

    def set_automatic(self, auto: bool):
        self._automatic = auto

    def get_commanded_speed(self) -> float:
        return self._command_speed

    def set_commanded_speed(self, speed: float):
        self._command_speed = speed

    # Testbench
    def set_authority(self, _authority: float):
        self._authority = _authority

    def get_authority(self) -> float:
        return self._authority

    def set_suggested_speed(self, _suggested_speed: float):
        self._suggested_speed = _suggested_speed

    def get_suggested_speed(self) -> float:
        return self._suggested_speed

    def set_test_speed_limit(self, _test_speed_limit: float):
        self._test_speed_limit = _test_speed_limit

    def get_test_speed_limit(self) -> float:
        return self._test_speed_limit

    def set_broken_rail(self, _broken_rail: bool):
        self._broken_rail = _broken_rail

    def get_broken_rail(self) -> bool:
        return self._broken_rail

    def set_engine_failure(self, _engine_failure: bool):
        self._engine_failure = _engine_failure

    def get_engine_failure(self) -> bool:
        return self._engine_failure

    def set_circuit_failure(self, _circuit_failure: bool):
        self._circuit_failure = _circuit_failure

    def get_circuit_failure(self) -> bool:
        return self._circuit_failure

    def set_power_failure(self, _power_failure: bool):
        self._power_failure = _power_failure

    def get_power_failure(self) -> bool:
        return self._power_failure

    def set_railway_crossing(self, crossing, _crossing_lights_gates: int):
        self._crossing_lights_gates[crossing] = _crossing_lights_gates

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
