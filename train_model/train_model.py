# -- Imports -- #
import math
import random as rand
import numpy as np
import threading
# from Train_Model_Test_Bench_UI import Ui_TrainModel_TestBench as tb
# from Train_Model_UI import Ui_TrainModel_MainUI as Train_Model_UI
import threading

class TrainModel(object):
    def __init__(self):

        # -- Train Model Variables -- #
        self._cmd_power = 0.01 # commanded power
        self._actual_power = 0.00 # actual power
        self._force = 0.0 # force
        self._curr_passenger_count = 0 # passenger count currently on the train
        self._max_passenger_count = 222 # combine max standing & seating passengers
        self._prev_passenger_count = 0 # previous passenger count for the train
        self._passenger_mass = 0.0 # mass of the passengers on the train
        self._train_mass = 40900.0 # mass of the train empty
        self._total_mass = 0.0 # total mass of the train with passengers
        self._temp_sp = 0.0 # internal temperature set point
        self._temperature = 0.0 # internal temperature of the train
        self._local_time = 0
        self._time = [0]
        self._block = 0 # current block the train is on
        self._beacon = "" # beacon information
        self._line = "[COLOR]" # line the train is on

        # -- Failure Modes -- #
        self._ebrake_failure = False # ebrake failure
        self._engine_failure = False # train engine failure
        self._sbrake_failure = False # service brake failure
        self._signal_failure = False # signal pickup failure

        # -- Controls -- #
        self._right_door = False # right door
        self._left_door = False # left door
        self._int_lights = False # internal lights
        self._ext_lights = False # external lights
        self._emergency_brake = False  # emergency brake
        self._service_brake = False # service brake

        # -- Run the Update Function -- #
        self.update()

    def update(self, thread=False):
        ##################################
        # Input Train Controller Signals #
        ##################################
        # Commanded Power
        # TODO: change get_cmd_power to get_cmd_power from train controller signals
        self.set_cmd_power(float(self.get_cmd_power()))  # Pass input from test UI text box

        # Actual Power
        # TODO: change get_actual_power to get_actual_power from train controller signals
        self.set_actual_power(float(self.get_actual_power()))  # Pass input from test UI text box

        #################
        # Failure Modes #
        #################
        # E-Brake Failure
        # TODO: change get_ebrake_failure to get_ebrake_failure from train controller signals
        self.set_ebrake_failure(bool(self.get_ebrake_failure()))  # Pass input from test UI text box

        # Train Engine Failure
        # TODO: change get_engine_failure to get_engine_failure from train controller signals
        self.set_engine_failure(bool(self.get_engine_failure()))  # Pass input from test UI text box

        # Service Brake Failure
        # TODO: change get_sbrake_failure to get_sbrake_failure from train controller signals
        self.set_sbrake_failure(bool(self.get_sbrake_failure()))  # Pass input from test UI text box

        # Signal Pickup Failure
        # TODO: change get_signal_failure to get_signal_failure from train controller signals
        self.set_signal_failure(bool(self.get_signal_failure()))  # Pass input from test UI text box

        ############
        # Controls #
        ############
        # Right Door
        # TODO: change get_right_door to get_right_door from train controller signals
        self.set_right_door(bool(self.get_right_door()))  # Pass input from test UI text box

        # Left Door
        # TODO: change get_left_door to get_left_door from train controller signals
        self.set_left_door(bool(self.get_left_door()))  # Pass input from test UI text box

        # Internal Lights
        # TODO: change get_int_lights to get_int_lights from train controller signals
        self.set_int_lights(bool(self.get_int_lights()))  # Pass input from test UI text box

        # External Lights
        # TODO: change get_ext_lights to get_ext_lights from train controller signals
        self.set_ext_lights(bool(self.get_ext_lights()))  # Pass input from test UI text box

        # Emergency Brake
        # TODO: change get_emergency_brake to get_emergency_brake from train controller signals
        self.set_emergency_brake(bool(self.get_emergency_brake()))  # Pass input from test UI text box

        # Service Brake
        # TODO: change get_service_brake to get_service_brake from train controller signals
        self.set_service_brake(bool(self.get_service_brake()))  # Pass input from test UI text box

        #############################
        # Input Track Model Signals #
        #############################
        # Passenger Count
        # TODO: change get_curr_passenger_count to get_curr_passenger_count from track model signals
        self.set_curr_passenger_count(int(self.get_curr_passenger_count()))  # Pass input from test UI text box

        # Time
        # TODO: change get_time to get_time from track model signals
        self.set_time(self.get_time())

        # Beacon
        # TODO: change get_beacon to get_beacon from track model signals
        self.set_beacon(self.get_beacon())

        # Line
        # TODO: change get_line to get_line from track model signals
        self.set_line(self.get_line())

        # Block
        # TODO: change get_block to get_block from track model signals
        self.set_block(self.get_block())

        ##############################
        # Output to Train Controller #
        ##############################

        #########################
        # Output to Track Model #
        #########################

        #####################################
        # Internal Train Model Calculations #
        #####################################
        # Force
        # TODO: Fix get_force to calculate force based on Newton's Laws
        self.set_force(float(self.get_force()))  # Pass input from test UI text box

        # Passenger Mass
        self.set_passenger_mass(self.get_curr_passenger_count())

        # Total Mass
        self.set_total_mass()

        # Internal Temperature
        self.set_temperature(self.get_temperature())

    #     # Temperature
    #     self.set_temperature(self._temp_sp)
    #
        # Enable Threading
        if thread:
            threading.Timer(0.1, self.update).start()

    # -- Getters and Setters -- #
    # beacon
    def set_beacon(self, _beacon: str):
        self._beacon = _beacon

    def get_beacon(self) -> str:
        return self._beacon

    # line
    def set_line(self, _line: str):
        self._line = _line

    def get_line(self) -> str:
        return self._line

    # block
    def set_block(self, _block: int):
        self._block = _block

    def get_block(self) -> int:
        return self._block

    # time
    # TODO: Confirm if this needs to be a list or int (_time[0])
    def set_time(self, _time: list):
        self._time = _time

    # TODO: Confirm if this needs to be a list or int (_time[0])
    def get_time(self) -> list:
        return self._time

    # temperature
    # TODO: Fix get_temperature to calculate temp based on elapsed time
    def set_temperature(self, temp:float):
        if self._temp_sp != temp:
            self._local_time = self._time[0]
            self._temp_sp = temp
        self._temperature= round(self._temp_sp * (1 - math.exp(-(self._time[0] - self._local_time))), 0)
        print(self._temperature, self._temp_sp, self._time[0] - self._local_time)
    def get_temperature(self) -> float:
        return self._temperature

    # commanded power
    def set_cmd_power(self, _cmd_power: float):
        self._cmd_power = _cmd_power

    def get_cmd_power(self) -> float:
        return self._cmd_power

    # actual power
    def set_actual_power(self, _actual_power: float):
        self._actual_power = _actual_power

    def get_actual_power(self) -> float:
        return self._actual_power

    # force
    def set_force(self, _force: float):
        self._force = _force

    # TODO: calculate force based on Newton's Laws
    def get_force(self) -> float:
        return round(self._actual_power/self._cmd_power,3)

    # passenger count
    def set_curr_passenger_count(self, _curr_passenger_count: int):
        self._curr_passenger_count = _curr_passenger_count

    def get_curr_passenger_count(self) -> int:
        return self._curr_passenger_count

    # passenger mass
    def set_passenger_mass(self, _curr_passenger_count: float):
        self._passenger_mass = self._curr_passenger_count * 150 * 0.453592 # lbs to kg

    def get_passenger_mass(self) -> float:
        return self._passenger_mass

    # train mass
    def set_total_mass(self):
        self._total_mass = self._train_mass + self._passenger_mass

    def get_total_mass(self) -> float:
        return self._total_mass

    # Failure Modes
    # ebrake failure
    def set_ebrake_failure(self, _ebrake_failure: bool):
        self._ebrake_failure = _ebrake_failure

    def get_ebrake_failure(self) -> bool:
        return self._ebrake_failure

    # train engine failure
    def set_engine_failure(self, _engine_failure: bool):
        self._engine_failure = _engine_failure

    def get_engine_failure(self) -> bool:
        return self._engine_failure

    # service brake failure
    def set_sbrake_failure(self, _sbrake_failure: bool):
        self._sbrake_failure = _sbrake_failure

    def get_sbrake_failure(self) -> bool:
        return self._sbrake_failure

    # signal pickup failure
    def set_signal_failure(self, _signal_failure: bool):
        self._signal_failure = _signal_failure

    def get_signal_failure(self) -> bool:
        return self._signal_failure

    # Controls
    # right door
    def set_right_door(self, _right_door: bool):
        self._right_door = _right_door

    def get_right_door(self) -> bool:
        return self._right_door

    # left door
    def set_left_door(self, _left_door: bool):
        self._left_door = _left_door

    def get_left_door(self) -> bool:
        return self._left_door

    # internal lights
    def set_int_lights(self, _int_lights: bool):
        self._int_lights = _int_lights

    def get_int_lights(self) -> bool:
        return self._int_lights

    # external lights
    def set_ext_lights(self, _ext_lights: bool):
        self._ext_lights = _ext_lights

    def get_ext_lights(self) -> bool:
        return self._ext_lights

    # emergency brake
    def set_emergency_brake(self, _emergency_brake: bool):
        self._emergency_brake = _emergency_brake

    def get_emergency_brake(self) -> bool:
        return self._emergency_brake

    # service brake
    def set_service_brake(self, _service_brake: bool):
        self._service_brake = _service_brake

    def get_service_brake(self) -> bool:
        return self._service_brake