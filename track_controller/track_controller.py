class Track_Controller(object):

    def __init__(self):
        # self._blue = ["A1","A2","A3","A4","A5","B6","B7","B8","B9","B10","C11","C12","C13","C14","C15"]

        # 2 = Occupancy(1 = occupied, 0 = not occupied(defualt)), 1 = Speed Limit
        self._blue = {'A1': {1: 50, 2: 1}, 'A2': {1: 50, 2: 0}, 'A3': {1: 50, 2: 0}, 'A4': {1: 50, 2: 0},
                      'A5': {1: 50, 2: 0}, 'B6': {1: 50, 2: 0}, 'B7': {1: 50, 2: 0}, 'B8': {1: 50, 2: 0},
                      'B9': {1: 50, 2: 0}, 'B10': {1: 50, 2: 0}, 'C11': {1: 50, 2: 0}, 'C12': {1: 50, 2: 0},
                      'C13': {1: 50, 2: 0}, 'C14': {1: 50, 2: 0}, 'C15': {1: 50, 2: 0}}
        # 0 = red, 1 = green, 2 = super green
        self._lights = {'A5': 0, 'B6': 0, 'C11': 0}
        # plc input
        self._plc_input = ""
        # 0 = left, 1 = right
        self._switches = {'BC-A': 0}
        # crossing lights/gate
        self._crossing_lights_gates = ""
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
        self._suggested_speed = 0
        self._test_speed_limit = 0
        self._track_status = False
    # Variables

    def get_blue_track(self) -> dict:
        return self._blue

    def get_occupancy(self, block) -> int:
        return self._blue[block][2]

    def set_occupancy(self, block, value: int):
        self._blue[block][2] = value

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