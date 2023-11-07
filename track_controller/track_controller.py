import traceback

from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.track_controller_track_model_api import TrackControllerTrackModelAPI
class Track_Controller(object):

    def __init__(self, ctcsignals: CTCTrackControllerAPI, tracksignals: TrackControllerTrackModelAPI):
        # 2 = Occupancy(1 = occupied, 0 = not occupied(defualt)), 1 = Speed Limit
        self._blue = {'A1': {1: 50, 2: 1}, 'A2': {1: 50, 2: 0}, 'A3': {1: 50, 2: 0}, 'A4': {1: 50, 2: 0},
                      'A5': {1: 50, 2: 0}, 'B6': {1: 50, 2: 0}, 'B7': {1: 50, 2: 0}, 'B8': {1: 50, 2: 0},
                      'B9': {1: 50, 2: 0}, 'B10': {1: 50, 2: 0}, 'C11': {1: 50, 2: 0}, 'C12': {1: 50, 2: 0},
                      'C13': {1: 50, 2: 0}, 'C14': {1: 50, 2: 0}, 'C15': {1: 50, 2: 0}}
        #blocks that are currently occupied
        self._occupied_blocks = ['A1']
        # 1 = red, 0 = green
        self._lights = {'A5': 0, 'B6': 0, 'C11': 0}
        # plc input
        self._plc_input = ""
        # 1 = left, 0 = right
        self._switches = {'BC-A': 0}
        # crossing lights/gate
        self._crossing_lights_gates = {'A1': 0}
        # if program is in automatic mode
        self._automatic = False
        # commanded speed is speed limit - occupancy
        self._command_speed = 0

        # Testbench Variables
        self._broken_rail = False  # ebrake failure
        self._engine_failure = False  # train engine failure
        self._circuit_failure = False  # service brake failure
        self._power_failure = False  # signal pickup failure
        self._authority = 0
        self._suggested_speed = 30
        self._test_speed_limit = 0
        self._track_status = {'block': False}
        self._passengers = 0

        #api signals
        self.ctc_ctrl_signals = ctcsignals
        self.track_ctrl_signals = tracksignals
        try:
            self.update()
        except:
            print("Can't update")

    def update(self, thread=True):
        #Interal inputs
        self.set_commanded_speed(self.get_commanded_speed())

        #CTC Office Inputs
        # self.set_authority(self.ctc_ctrl_signals._authority) #TODO need to get from individual Train ID
        self.set_suggested_speed(self.ctc_ctrl_signals._suggested_speed)
        self.set_track_section_status(self.ctc_ctrl_signals._track_section_status)

        #CTC Office Outputs
        self.ctc_ctrl_signals._passenger_onboarding = self.get_passengers()
        self.ctc_ctrl_signals._occupancy = self.get_block_occupancy()

        #Track Model Inputs
        self.set_broken_rail(self.track_ctrl_signals._broken_rail)
        self.set_engine_failure(self.track_ctrl_signals._engine_failure)
        self.set_circuit_failure(self.track_ctrl_signals._circuit_failure)
        self.set_power_failure(self.track_ctrl_signals._power_failure)
        self.set_blue_track(self.track_ctrl_signals._blue)
        # wait until we have things connected to mess around with this
        # self.set_blue_track(self.track_ctrl_signals._green)

        #Track Model Outputs
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

    def set_passengers(self, tickets):
        self._passengers = tickets

    def get_track_section_status(self):
        return self._track_status
    def set_track_section_status(self, block):
        self._track_status = block
        for i in block.keys():
            self._blue[i][2] = int(block[i])

    def get_blue_track(self) -> dict:
        return self._blue

    def set_blue_track(self, track):
        self._blue = track

    def get_occupancy(self, block) -> int:
        return self._blue[block][2]

    def get_block_occupancy(self) -> dict:
        temp = {}
        for x in self._occupied_blocks:
            temp.update({x:self.get_occupancy(x)})
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

    def get_speed_limit(self, block) -> float:
        return self._blue[block][1]

    def set_speed_limit(self, block, value: float):
        self._blue[block][1] = value

    def get_switch_list(self) -> dict:
        return self._switches

    def get_switch(self, switch) -> int:
        return self._switches[switch]

    def set_switch(self, switch, value: int):
        self._switches[switch] = value

    def get_lights(self, light) -> int:
        return self._lights[light]

    def set_lights(self, light, value: int):
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