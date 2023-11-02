import traceback

import serial

from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.track_controller_track_model_api import TrackControllerTrackModelAPI


class Track_Controller_HW(object):

    def __init__(self, ctcsignals: CTCTrackControllerAPI, tracksignals: TrackControllerTrackModelAPI):
        # self._blue = ["A1","A2","A3","A4","A5","B6","B7","B8","B9","B10","C11","C12","C13","C14","C15"]

        # 2 = Occupancy(1 = occupied, 0 = not occupied(defualt)), 1 = Speed Limit,
        self._blue = {'A1': {1: 50, 2: 0}, 'A2': {1: 50, 2: 0}, 'A3': {1: 50, 2: 0}, 'A4': {1: 50, 2: 0},
                      'A5': {1: 50, 2: 0}, 'B6': {1: 50, 2: 0}, 'B7': {1: 50, 2: 0}, 'B8': {1: 50, 2: 0},
                      'B9': {1: 50, 2: 0}, 'B10': {1: 50, 2: 0}, 'C11': {1: 50, 2: 0}, 'C12': {1: 50, 2: 0},
                      'C13': {1: 50, 2: 0}, 'C14': {1: 50, 2: 0}, 'C15': {1: 50, 2: 0}}
        self._green = {}
        # 0 = red, 1 = green, 2 = super green
        self._lights = {'A5': 0, 'B6': 0, 'C11': 0}
        # plc input
        self._plc_input = ""
        # 0 = left, 1 = right
        self._switches = {'A5': 0}
        # crossing lights/gate
        self._crossing_lights_gates = {}
        # if program is in automatic mode
        self._automatic = False
        # commanded speed is speed limit - occupancy
        self._command_speed = 0#{'A1': {1: 50}, 'A2': {1: 50}, 'A3': {1: 50}, 'A4': {1: 50},
                               #'A5': {1: 50}, 'B6': {1: 50}, 'B7': {1: 50}, 'B8': {1: 50},
                               #'B9': {1: 50}, 'B10': {1: 50}, 'C11': {1: 50}, 'C12': {1: 50},
                               #'C13': {1: 50}, 'C14': {1: 50}, 'C15': {1: 50}}

        self._occupied_blocks = []

        self._ard = serial.Serial(port='COM5', baudrate=9600, timeout=.1)


        # Testbench Variables
        self._broken_rail = False  # ebrake failure
        self._engine_failure = False  # train engine failure
        self._circuit_failure = False  # service brake failure
        self._power_failure = False  # signal pickup failure
        self._authority = 0
        self._suggested_speed = 0
        self._test_speed_limit = 0
        self._track_status = False
        self._passengers = 0

        self.ctc_ctrl_signals = ctcsignals
        self.track_ctrl_signals = tracksignals

        self.update()

    # Variables
    def update(self, thread=False):
        # Interal inputs
        self.set_commanded_speed(self.get_commanded_speed())

        # CTC Office Inputs
        # self.set_authority(self.ctc_ctrl_signals._authority) #TODO need to get from individual Train ID
        self.set_suggested_speed(self.ctc_ctrl_signals._suggested_speed)
        self.set_track_section_status(self.ctc_ctrl_signals._track_section_status)

        # CTC Office Outputs
        self.ctc_ctrl_signals._passenger_onboarding = self.get_passengers()
        self.ctc_ctrl_signals._occupancy = self.get_block_occupancy()

        # Track Model Inputs
        self.set_broken_rail(self.track_ctrl_signals._broken_rail)
        self.set_engine_failure(self.track_ctrl_signals._engine_failure)
        self.set_circuit_failure(self.track_ctrl_signals._circuit_failure)
        self.set_power_failure(self.track_ctrl_signals._power_failure)
        self.set_blue_track(self.track_ctrl_signals._blue)
        # wait until we have things connected to mess around with this
        # self.set_blue_track(self.track_ctrl_signals._green)
        self.set_green_track(self.track_ctrl_signals._green)

        # Track Model Outputs
        self.track_ctrl_signals._authority = self.get_authority()
        self.track_ctrl_signals._commanded_speed = self.get_commanded_speed()
        # for i in self._lights.keys():
        #     self.track_ctrl_signals._blue[i][5] = self.get_lights(i)
        # for i in self._switches.keys():
        #     self.track_ctrl_signals._blue[i][4] = self.get_switch(i)
        # for i in self._crossing_lights_gates.keys():
        #     self.track_ctrl_signals._blue[i][3] = self.get_railway_crossing(i)
        #

    def get_passengers(self):
        return self._passengers

    def send_update(self, block_number: str):
        send_string = "1"
        if len(block_number) == 2:
            send_string += "00" + block_number
        elif len(block_number) == 3:
            send_string += "0" + block_number
        elif len(block_number) == 4:
            send_string += block_number
        command = str(self.get_commanded_speed())
        if len(command) == 1:
            send_string += "0" + command
        elif len(command) == 2:
            send_string += command
        if block_number in self.get_light_list():
            send_string += "1"
            if self.get_lights(block_number) == 1:
                send_string += "1"
            elif self.get_lights(block_number) == 0:
                send_string += "0"
        else:
            send_string += "00"
        if block_number in self.get_switch_list():
            send_string += "1"
            if self.get_switch(block_number) == 1:
                send_string += "1"
            elif self.get_switch(block_number) == 0:
                send_string += "0"
        else:
            send_string += "00"
        send_string += "00"
        self.get_ard().write(send_string.encode('utf-8'))
        print(send_string)

    def get_ard(self):
        return self._ard

    def set_passengers(self, tickets):
        self._passengers = tickets

    def get_track_section_status(self):
        return self._track_status

    def set_track_section_status(self, block):
        self._track_status = block
        for i in block.keys():
            self._blue[i][2] = block[i]

    def get_crossing_lights_gates(self) -> dict:
        return self._crossing_lights_gates

    def set_crossing_lights_gate(self, light: str, value: int):
        self._crossing_lights_gates[light] = value

    def get_blue_track(self) -> dict:
        return self._blue

    def set_blue_track(self, track):
        self._blue = track

    def get_green_track(self) -> dict:
        return self._green

    def set_green_track(self, track):
        self._green = track

    def get_block_occupancy(self) -> dict:
        temp = {}
        for x in self._occupied_blocks:
            temp.update({x: self.get_occupancy(x)})
        return temp

    def get_occupied_blocks(self) -> list:
        temp = []
        for x in self._occupied_blocks:
            temp.append(x + '          ' + str(self.get_speed_limit(x)) + ' mph')
        return temp

    def set_occupancy(self, block, value: int):
        self._blue[block][2] = value
        if value == 1:
            self._occupied_blocks.append(block)
        else:
            self._occupied_blocks.remove(block)
        self._occupied_blocks.sort()

    def get_occupancy(self, block) -> int:
        return self._blue[block][2]

    def get_speed_limit(self, block) -> float:
        return self._blue[block][1]

    def set_speed_limit(self, block, value: float):
        self._blue[block][1] = value

    def get_switch_list(self) -> dict:
        return self._switches

    def get_switch(self, switch) -> int:
        return self._switches[switch]

    def set_switch(self, value: int, switch: str):
        self._switches[switch] = value

    def get_light_list(self) -> dict:
        return self._lights

    def get_lights(self, light) -> int:
        return self._lights[light]

    def set_lights(self, value: int, light: str):
        self._lights[light] = value

    def get_automatic(self) -> bool:
        return self._automatic

    def set_automatic(self, auto: bool):
        self._automatic = auto

    def get_commanded_speed(self) -> float:
        return self._command_speed

    def set_commanded_speed(self, speed: float):
        self._command_speed = speed

    # Testbench
    def set_authority(self, _authoirty: float):
        self._authority = _authoirty

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

    def launch_ui(self):
        print("Launching Track Controller HW UI")
        try:
            from track_controller_hw.Track_Controller_HW_UI import Ui_track_controller_mainwindow
            self._ui = Ui_track_controller_mainwindow(self)
        except Exception as e:
            print("An error occurred:")
            traceback.print_exc()
            print("Train model not initialized yet")
