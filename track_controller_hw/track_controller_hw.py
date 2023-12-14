import os
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

        # green line track
        self._green = {}


        # used to make sure plc is loaded
        self._plc_set = False

        # time
        self._time = 0

        self._train_ids = {}
        # 0 = red, 1 = green, 2 = super green
        self._lights = {'A1': 0, 'D13': 0, 'F28': 0, 'Z150': 0}
        # plc input
        self._plc_input = ""
        # 0 = right, 1 = left
        self._switches = {'D13': 0, 'F28': 0, 'I57': 0}
        # crossing lights/gate
        self._crossing_lights_gates = {'E19': 0}
        # if program is in automatic mode
        self._automatic = True

        self._previous = False
        # commanded speed is speed limit - occupancy
        self._command_speed = 0  # {'A1': {1: 50}, 'A2': {1: 50}, 'A3': {1: 50}, 'A4': {1: 50},
        # 'A5': {1: 50}, 'B6': {1: 50}, 'B7': {1: 50}, 'B8': {1: 50},
        # 'B9': {1: 50}, 'B10': {1: 50}, 'C11': {1: 50}, 'C12': {1: 50},
        # 'C13': {1: 50}, 'C14': {1: 50}, 'C15': {1: 50}}

        # list of occupied blocks to show on UI
        self._previous_blocks = []

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

        self._occupancy_timer = 0
        # self._passengers = 0

        # signals from the APIs to get/set
        self.ctc_ctrl_signals = ctcsignals
        self.track_ctrl_signals = tracksignals
        self._start_up = 0
        self._plc_logic = File_Parser(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "track_controller_hw", "PLC1.txt")))

        self.update()

    # Variables
    def update(self, thread=True):

        # sends PLC to Arduino after 100 cycles
        if self.get_start_up() == 100:
            #self.get_plc_logic().parse()
            send = "1"
            send += self.get_plc_logic().parse()
            send += "\n"
            print("Serial: " + send)
            self.get_ard().write(send.encode('utf-8'))
            self.set_start_up(self.get_start_up() + 1)
        self.set_start_up(self.get_start_up() + 1)
        self.set_commanded_speed(self.get_commanded_speed())

        self.set_time(self.ctc_ctrl_signals._time)

        # used to recieve info from the Ardunio
        self.receive()

        #sets the automatic variable
        self.set_previous(self.get_automatic())

        # checks to see if in automatic or in manual mode -if in automatic -> run PLC
        if self.get_automatic() and self.get_plc_set():
            send_string = "1"
            send_string += self.get_plc_logic().parse()
            send_string += "\n"
            print("Serial: " + send_string)
            self.get_ard().write(send_string.encode('utf-8'))
            self.set_plc_set(False)


        #sent block occupancy from Track Model
        self.set_previous_blocks(self.track_ctrl_signals._occupancy["Green"])
        self.set_track_section_status(self.ctc_ctrl_signals._track_section_status["green"])
        self.set_occupied(self.get_previous_blocks())
        self.get_previous_blocks().sort()

        if self.get_occupancy_timer() != 10:
            self.set_occupancy_timer(self.get_occupancy_timer() + 1)
        elif self.get_occupancy_timer() == 10:
            self.send_occupied()
            self.set_occupancy_timer(0)


        try:
            self.track_ctrl_signals._train_ids = self.ctc_ctrl_signals._train_ids
            self.track_ctrl_signals._train_lines = self.ctc_ctrl_signals._train_lines
            self.track_ctrl_signals._train_out = self.ctc_ctrl_signals._train_out
            self.ctc_ctrl_signals._train_in = self.track_ctrl_signals._train_in
            self.ctc_ctrl_signals._filepath = self.track_ctrl_signals._filepath
        except Exception as e:
            print("Cannot pass train info")
        """"
        try:
            #for maintance mode in CTC
            self.set_track_section_status(self.ctc_ctrl_signals._track_section_status["green"])
        except Exception as e:
            print(e)
        print("Prev:" + str(self.get_previous_blocks()))
        print("Occ:" + str(self.get_occupied()))

        # checks to see if occupancy changed, if it did then send new occupancy to Arduino
        if self.get_occupied() != self.get_previous_blocks():
            self.set_occupied(self.get_previous_blocks())
            self.send_occupied()
        
        #sends Occupancy from CTC
        self.ctc_ctrl_signals._occupancy["Green"] = self._occupied_blocks
        """
        if thread:
            threading.Timer(.1, self.update).start()

    def send_occupied(self):
        occupied = "2"
        for i in self.get_occupied():
            occupied += " " + str(i)
        print(occupied)
        occupied += "\n"
        self.get_ard().write(occupied.encode('utf-8'))

    # used to recieve info from the Ardunio
    def receive(self):
        try:
            if self.get_ard().inWaiting() > 0:
                data_bytes = self.get_ard().readline()
                data_str = data_bytes.decode('utf-8').strip()
                #print(f"From Serial: {data_str}")
                commands = data_str.split()

                for command in commands:
                    # Split each command into switch/light and value
                    identifier, value_str = command.split('/')
                    value = int(value_str)

                    # Check if it's a switch or light and call the appropriate set function
                    if identifier[0] == "0":
                        if identifier[1:] in self._switches:
                            self.set_switch(identifier[1:], value)
                        else:
                            print(f"Unknown identifier Rest: {identifier}")
                    elif identifier[0] == "1":
                        if identifier[1:] in self._lights:
                            self.set_lights(identifier[1:], value)
                        else:
                            print(f"Unknown identifier Rest: {identifier}")
                    else:
                        print(f"Unknown identifier First: {identifier}")

        except Exception as e:
            print("An error occurred:")
            traceback.print_exc()

    # send which block should be displayed in ardunio
    def select_block(self, block_number):
        block_send = "0" + block_number + "\n"
        self.get_ard().write(block_send.encode('utf-8'))
        print(block_send)

    def get_occupancy_timer(self):
        return self._occupancy_timer

    def set_occupancy_timer(self, occupancy_time):
        self._occupancy_timer = occupancy_time

    def set_track_section_status(self, blocks):
        for block in blocks:
            self.set_occupancy(block, blocks.count(block))

    def get_start_up(self) -> int:
        return self._start_up

    def set_start_up(self, set: int):
        self._start_up = set

    def get_plc_set(self):
        return self._plc_set

    def set_plc_set(self, set_bool: bool):
        self._plc_set = set_bool

    def get_plc_logic(self):
        return self._plc_logic

    def set_plc_logic(self, parse):
        self._plc_logic = parse

    def get_block_occupancy(self) -> dict:
        temp = {}
        for x in self._occupied_blocks:
            temp.update({x: self.get_occupancy(x)})
        return temp

    def get_occupied(self):
        return self._occupied_blocks

    def get_occupancy(self, block) -> bool:
        return self._occupied_blocks.count(block)

    def set_occupied(self, blocks: list):
        self._occupied_blocks = blocks

    def set_previous_blocks(self, blocks: list):
        self._previous_blocks = blocks

    def get_previous_blocks(self):
        return self._previous_blocks

    def get_occupied_blocks(self) -> list:
        temp = []
        for x in self._occupied_blocks:
            temp.append(x + '          ' + str(self.get_speed_limit(x)) + ' mph')
        return temp

    def set_occupancy(self, block, value: int):
        if self._occupied_blocks.count(block) < 1 and value == 1:
            self._occupied_blocks.append(block)
            print("Add Occupied")
        elif self._occupied_blocks.count(block) > 0 and value == 0:
            self._occupied_blocks.remove(block)
            print("Remove Occupied")
        if self._previous_blocks.count(block) < 1 and value == 1:
            self._previous_blocks.append(block)
            print("Add Previous")
        elif self._previous_blocks.count(block) > 0 and value == 0:
            self._previous_blocks.remove(block)
            print("Add Previous")
        self._occupied_blocks.sort()
        self._previous_blocks.sort()

    def get_switch_list(self) -> dict:
        return self._switches

    def get_switch(self, switch):
        return self._switches[switch]

    def set_switch(self, switch, value: int):
        try:
            self._switches[switch] = value
            swit = switch[1:]
            self.ctc_ctrl_signals._switch["Green"][swit] = value
            self.track_ctrl_signals._switches["Green"][swit] = value
        except Exception as e:
            print("Invalid switch")

    def get_lights(self, line):
        return self._lights[line]

    def get_lights_list(self) -> dict:
        return self._lights

    def set_lights(self, light: str, value: int):
        try:
            self._lights[light] = value
            lit = light[1:]
            self.ctc_ctrl_signals._light["Green"][lit] = value
            self.track_ctrl_signals._lights["Green"][lit] = value
        except Exception as e:
            print("Invalid light")

    def get_automatic(self) -> bool:
        return self._automatic

    def set_automatic(self, auto: bool):
        self._automatic = auto

    def get_previous(self) -> bool:
        return self._previous

    def set_previous(self, auto: bool):
        self._previous = auto

    #Testbench Varibales Below(Not in use)
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

    def get_crossing_lights_gates(self) -> dict:
        return self._crossing_lights_gates

    def set_train_out(self, trains: dict):
        self._train_info = trains

    def get_train_out(self):
        return self._train_info

    def set_authority(self, train: int, authority: int):
        self._train_info[train][0] = authority

    def get_authority(self, train: int) -> int:
        return self._train_info[train][0]

    def set_suggested_speed(self, train: int, _suggested_speed: int):
        self._train_info[train][1] = _suggested_speed

    def get_suggested_speed(self, train: int) -> float:
        return self._train_info[train][1]

    def get_crossing_lights_gates_select(self, value):
        return self._crossing_lights_gates[value]

    def set_crossing_lights_gate(self, light: str, value: int):
        self._crossing_lights_gates[light] = value

    def get_green_track(self) -> dict:
        return self._green

    def set_green_track(self, track):
        self._green = track

    def get_time(self):
        return self._time

    def set_time(self, times):
        self._time = times

    def get_speed_limit(self, block) -> float:
        return self._green[block][1]

    def set_speed_limit(self, block, value: float):
        self._green[block][1] = value

    def get_commanded_speed(self) -> float:
        return self._command_speed

    def set_commanded_speed(self, speed: float):
        self._command_speed = speed

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
