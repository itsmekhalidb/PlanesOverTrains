import threading
import traceback
import datetime

import serial
import time

from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.track_controller_track_model_api import TrackControllerTrackModelAPI
from track_controller_hw.File_Parser import File_Parser


class Track_Controller_HW(object):

    def __init__(self, ctcsignals: CTCTrackControllerAPI, tracksignals: TrackControllerTrackModelAPI):

        # 2 = Occupancy(1 = occupied, 0 = not occupied(defualt)), 1 = Speed Limit,
        self._blue = {'A1': {1: 50, 2: 0}, 'A2': {1: 50, 2: 0}, 'A3': {1: 50, 2: 0}, 'A4': {1: 50, 2: 0},
                      'A5': {1: 50, 2: 0}, 'B6': {1: 50, 2: 0}, 'B7': {1: 50, 2: 0}, 'B8': {1: 50, 2: 0},
                      'B9': {1: 50, 2: 0}, 'B10': {1: 50, 2: 0}, 'C11': {1: 50, 2: 0}, 'C12': {1: 50, 2: 0},
                      'C13': {1: 50, 2: 0}, 'C14': {1: 50, 2: 0}, 'C15': {1: 50, 2: 0}}

        # green line track
        self._green = {}

        # plc object
        self.blue_line_plc = File_Parser("")

        # used to make sure plc is loaded
        self._plc_set = False

        # time
        self._time = 0

        self._train_ids = {}
        # 0 = red, 1 = green, 2 = super green
        self._lights = {'M77': 0, 'R101': 0, 'Q100': 0, 'N85': 0, 'K63': 0}
        # plc input
        self._plc_input = ""
        # 0 = right, 1 = left
        self._switches = {'M77': 0, 'N85': 0, 'K63': 0}
        # crossing lights/gate
        self._crossing_lights_gates = {}
        # if program is in automatic mode
        self._automatic = True

        self._previous = False
        # commanded speed is speed limit - occupancy
        self._command_speed = 0  # {'A1': {1: 50}, 'A2': {1: 50}, 'A3': {1: 50}, 'A4': {1: 50},
        # 'A5': {1: 50}, 'B6': {1: 50}, 'B7': {1: 50}, 'B8': {1: 50},
        # 'B9': {1: 50}, 'B10': {1: 50}, 'C11': {1: 50}, 'C12': {1: 50},
        # 'C13': {1: 50}, 'C14': {1: 50}, 'C15': {1: 50}}

        # list of occupied blocks to show on UI
        self._previous_blocks = ['A1']
        self._occupied_blocks = []
        # serial port connection object
        self._ard = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

        # Testbench Variables
        # self._broken_rail = False  # ebrake failure
        # self._engine_failure = False  # train engine failure
        # self._circuit_failure = False  # service brake failure
        # self._power_failure = False  # signal pickup failure
        self._authority = 0
        self._authority_blocks = {}
        self._suggested_speed_blocks = {}
        self._suggested_speed = 0
        # self._test_speed_limit = 0
        self._track_status = False
        # self._passengers = 0

        # signals from the APIs to get/set
        self.ctc_ctrl_signals = ctcsignals
        self.track_ctrl_signals = tracksignals

        self.update()

    # Variables
    def update(self, thread=True):
        # Interal inputs
        self.set_commanded_speed(self.get_commanded_speed())

        # CTC Office Inputs
        # self.set_authority(self.ctc_ctrl_signals._authority) #TODO need to get from individual Train ID
        self.set_suggested_speed(self.ctc_ctrl_signals._suggested_speed)
        #        self.set_track_section_status(self.ctc_ctrl_signals._track_section_status)

        # CTC Office Outputs
        #        self.ctc_ctrl_signals._passenger_onboarding = self.get_passengers()
        self.ctc_ctrl_signals._occupancy = self.get_block_occupancy()
        self.set_time(self.ctc_ctrl_signals._time)

        # Track Model Inputs
        #        self.set_broken_rail(self.track_ctrl_signals._broken_rail)
        #        self.set_engine_failure(self.track_ctrl_signals._engine_failure)
        #        self.set_circuit_failure(self.track_ctrl_signals._circuit_failure)
        #        self.set_power_failure(self.track_ctrl_signals._power_failure)
        self.set_blue_track(self.track_ctrl_signals._blue)
        # wait until we have things connected to mess around with this
        # self.set_blue_track(self.track_ctrl_signals._green)
        self.set_green_track(self.track_ctrl_signals._green)


        # Track Model Outputs
        self.track_ctrl_signals._authority = self.get_authority()
        self.track_ctrl_signals._commanded_speed = self.get_commanded_speed()
        """
        for i in self.ctc_ctrl_signals._train_info:
            self._suggested_speed_blocks.clear()
            self._suggested_speed_blocks[i] = self.ctc_ctrl_signals._train_info[i][1]
            self._authority_blocks.clear()
            self._authority_blocks[i] = self.ctc_ctrl_signals._train_info[i][2]
        """
        # for i in self._lights.keys():
        #     self.track_ctrl_signals._blue[i][5] = self.get_lights(i)
        # for i in self._switches.keys():
        #     self.track_ctrl_signals._blue[i][4] = self.get_switch(i)
        # for i in self._crossing_lights_gates.keys():
        #     self.track_ctrl_signals._blue[i][3] = self.get_railway_crossing(i)
        #

        # used to recieve info from the Ardunio

        self.receive()

        if self.get_automatic() != self.get_previous():
            if not self.get_automatic():
                self.get_ard().write("3".encode('utf-8'))
            else:
                self.get_ard().write("4".encode('utf-8'))

        self.set_previous(self.get_automatic())

        # checks to see if in automatic or in manual mode -if in automatic -> run PLC
        if self.get_automatic() and self.get_plc_set():
            print("get plc = true and automatic = true")
            self.get_plc()

        if self.get_occupied_blocks() != self._previous_blocks:
            self.set_occupied_blocks(self.track_ctrl_signals._train_occupancy)
            self.send_occupied()
            self._previous_blocks = self.get_occupied_blocks()

        if thread:
            threading.Timer(.1, self.update).start()

        time.sleep(.1)

    #   def get_passengers(self):
    #       return self._passengers

    def send_occupied(self):
        occupied = "2"
        for i in self.get_occupied():
            occupied += " " + i[1:]
        print(occupied)
        self.get_ard().write(occupied.encode('utf-8'))

    def get_train_id(self):
        return self._train_ids

    # used to recieve info from the Ardunio
    def receive(self):
        try:
            if self.get_ard().inWaiting() > 0:
                data_bytes = self.get_ard().readline()
                data_str = data_bytes.decode('utf-8').strip()
                print(data_str)
                count = 0
                for key in self.get_switch_list():
                    if data_str[count].isdigit():
                        self.set_switch(int(data_str[count]), key)
                        count += 1
                for key in self.get_light_list():
                    if data_str[count].isdigit():
                        self.set_lights(int(data_str[count]), key)
                        count += 1


        except Exception as e:
            print("An error occurred:")
            traceback.print_exc()

    # when in manual mode, used to send switch/light info to ardunio to update functions
    def send_update(self, block_number: str):
        send_string = "1"
        """
        if len(block_number) == 2:
            send_string += "00" + block_number
        elif len(block_number) == 3:
            send_string += "0" + block_number
        elif len(block_number) == 4:
            send_string += block_number
        """
        commanded = str(self.get_commanded_speed())
        if len(commanded) == 1:
            send_string += "0" + commanded
        elif len(commanded) == 2:
            send_string += commanded
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
        send_string += block_number
        self.get_ard().write(send_string.encode('utf-8'))
        print(send_string)
        time.sleep(3)
        self.select_block(block_number)

    # send which block should be displayed in ardunio
    def select_block(self, block_number):
        block_send = "0" + block_number
        self.get_ard().write(block_send.encode('utf-8'))
        print(block_send)

    def get_plc_set(self):
        return self._plc_set

    def set_plc_set(self, set_bool: bool):
        self._plc_set = set_bool

    def set_blue_plc(self, plc):
        self.blue_line_plc = plc

    def get_blue_plc(self):
        return self.blue_line_plc

    def get_authority_blocks(self):
        return self._authority_blocks

    def set_authority_blocks(self, train: str, value: float):
        self._authority_blocks[train] = value

    def get_suggested_speed_blocks(self):
        return self._suggested_speed_blocks

    def set_suggested_speed_blocks(self, train: str, value: float):
        self._suggested_speed_blocks[train] = value

    def get_ard(self):
        return self._ard

    def get_track_section_status(self):
        return self._track_status

    """ 
    def set_track_section_status(self, block):
        self._track_status = block
        for i in block.keys():
            self._blue[i][2] = block[i]
    """

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

    def get_occupied(self) -> list:
        return self._occupied_blocks

    def set_occupied_blocks(self, blocks: dict):
        self._occupied_blocks = blocks

    def get_occupied_blocks(self) -> list:
        temp = []
        for x in self._occupied_blocks:
            temp.append(x + '          ' + str(self.get_speed_limit(x)) + ' mph')
        return temp

    def set_occupancy(self, block, value: int):
        self._green[block][2] = value
        self.ctc_ctrl_signals._green[block][2] = value
        if value == 1:
            self._occupied_blocks.append(block)
        else:
            self._occupied_blocks.remove(block)
        self._occupied_blocks.sort()

    def get_occupancy(self, block) -> int:
        return self._green[block][2]

    def get_time(self):
        return self._time

    def set_time(self, times):
        self._time = times

    def get_plc(self):  # have not tested this yet
        print("In plc function")
        if self.blue_line_plc.parse():
            print("parse = true")
        """
            for i in range(len(self.blue_line_plc.get_block_number())):
                block_number = self.blue_line_plc.get_block_number()[i]
                block_occupancy = self.blue_line_plc.get_block_occupancy()[i]
                operation = self.blue_line_plc.get_operations()[i]
                operation_number = self.blue_line_plc.get_operations_number()[i]
                if ((block_occupancy == 'block' and 1 == self.track_controller_hw.get_occupancy(block_number)) or
                        (block_occupancy == '!block' and 0 == self.track_controller_hw.get_occupancy(block_number))):
                    if operation == 'switch':
                        self.track_controller_hw.set_switch(1, operation_number)
                    elif operation == '!switch':
                        self.track_controller_hw.set_switch(0, operation_number)
                    elif operation == "green":
                        self.track_controller_hw.set_lights(1, operation_number)
                    elif operation == "red":
                        self.track_controller_hw.set_lights(0, operation_number)
            """

        """""
            self.track_controller_hw.set_commanded_speed(
                min(self.track_controller_hw.get_suggested_speed(), self.track_controller_hw.get_speed_limit('B-A1')))

            self.sect_A_occ = bool(self.track_controller_hw.get_occupancy('B-A1') or self.track_controller_hw.get_occupancy(
                'B-A2') or self.track_controller_hw.get_occupancy('B-A3') or self.track_controller_hw.get_occupancy(
                'B-A4') or self.track_controller_hw.get_occupancy('B-A5'))
            self.sect_B_occ = bool(self.track_controller_hw.get_occupancy('B-B6') or self.track_controller_hw.get_occupancy(
                'B-B7') or self.track_controller_hw.get_occupancy('B-B8') or self.track_controller_hw.get_occupancy(
                'B-B9') or self.track_controller_hw.get_occupancy('B-B10'))
            self.sect_C_occ = bool(
                self.track_controller_hw.get_occupancy('B-C11') or self.track_controller_hw.get_occupancy(
                    'B-C12') or self.track_controller_hw.get_occupancy('B-C13') or self.track_controller_hw.get_occupancy(
                    'B-C14') or self.track_controller_hw.get_occupancy('B-C15'))
            if self.sect_A_occ:
                self.plc_output.addItem("Train detected in section A")
                self.track_controller_hw.set_lights(0, 'Light B-A5')
                self.track_controller_hw.set_lights(1, 'Light B-B6')
                self.track_controller_hw.set_lights(1, 'Light C-C11')
                if self.sect_B_occ:
                    self.plc_output.addItem("Train detected in section B")
                    self.track_controller_hw.set_lights(0, 'Light B-A5', )
                    self.track_controller_hw.set_lights(1, 'Light B-B6')
                    self.track_controller_hw.set_lights(1, 'Light B-C11')
                    self.track_controller_hw.set_switch(1, 'Switch BC-A')
                    self.plc_output.addItem("Stopping traffic from track section B")
                    self.plc_output.addItem("Switching to track section C")
                elif self.sect_C_occ:
                    self.plc_output.addItem("Train detected in section C")
                    self.track_controller_hw.set_lights(0, 'Light B-A5')
                    self.track_controller_hw.set_lights(1, 'Light B-B6')
                    self.track_controller_hw.set_lights(1, 'Light B-C11')
                    self.track_controller_hw.set_switch(0, 'Switch BC-A')
                    self.plc_output.addItem("Stopping traffic from track section C")
                    self.plc_output.addItem("Switching to track section B")
                else:
                    self.plc_output.addItem("Stopping traffic from track sections B and C")
                    self.plc_output.addItem("Switching to track section B")
            elif self.sect_B_occ:
                self.plc_output.addItem("Train detected in section B")
                self.track_controller_hw.set_lights(0, 'Light B-A5')
                self.track_controller_hw.set_lights(1, 'Light B-B6')
                self.track_controller_hw.set_lights(0, 'Light B-C11')
                self.track_controller_hw.set_switch(0, 'Light BC-A')
                self.plc_output.addItem("Stopping traffic from track sections A and C")
                self.plc_output.addItem("Switching to track section B")
            elif self.sect_C_occ:
                self.plc_output.addItem("Train detected in section C")
                self.track_controller_hw.set_lights(0, 'Light B-A5')
                self.track_controller_hw.set_lights(0, 'Light B-B6')
                self.track_controller_hw.set_lights(1, 'Light B-C11')
                self.track_controller_hw.set_switch(1, 'Switch BC-A')
                self.plc_output.addItem("Stopping traffic from track sections A and B")
                self.plc_output.addItem("Switching to track section C")
            else:
                self.plc_output.addItem("No trains on the track")
                self.track_controller_hw.set_lights(0, 'Light B-A5')
                self.track_controller_hw.set_lights(0, 'Light B-B6')
                self.track_controller_hw.set_lights(0, 'Light B-C11')
    """

    def get_speed_limit(self, block) -> float:
        return self._green[block][1]

    def set_speed_limit(self, block, value: float):
        self._green[block][1] = value

    def get_switch_list(self) -> dict:
        return self._switches

    def get_switch(self, switch) -> int:
        return self._switches[switch]

    def set_switch(self, value: int, switch: str):
        self._switches[switch] = value
        swit = switch[1:]
        self.ctc_ctrl_signals._switch[swit] = value
        self.track_ctrl_signals._switches[swit] = value

    def get_light_list(self) -> dict:
        return self._lights

    def get_lights(self, light) -> int:
        return self._lights[light]

    def set_lights(self, value: int, light: str):
        self._lights[light] = value
        swit = light[1:]
        self.ctc_ctrl_signals._light[swit] = value
        self.track_ctrl_signals._lights[swit] = value

    def get_automatic(self) -> bool:
        return self._automatic

    def set_automatic(self, auto: bool):
        self._automatic = auto

    def get_previous(self) -> bool:
        return self._previous

    def set_previous(self, auto: bool):
        self._previous = auto

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

    """
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
    """

    # used to launch UI from launcher
    def launch_ui(self):
        print("Launching Track Controller HW UI")
        try:
            from track_controller_hw.Track_Controller_HW_UI import Ui_track_controller_mainwindow
            self._ui = Ui_track_controller_mainwindow(self)
        except Exception as e:
            print("An error occurred:")
            traceback.print_exc()
            print("Train model not initialized yet")
