# -- Imports -- #
import math
import os
import random
import time
import random as rand
import numpy as np
import threading
# from Train_Model_Test_Bench_UI import Ui_TrainModel_TestBench as tb
# from Train_Model_UI import Ui_TrainModel_MainUI as Train_Model_UI
import threading

# TODO: Format Force and Power to be centered

class TrainModel(object):
    def __init__(self):

        # -- Train Model Variables -- #
        self._friction_coeff = 0.006 # friction coefficient for rails
        self._cmd_power = 0.0 # commanded power
        self._max_power = 120000.0 # max power of the train from data sheet
        self._force = 0.0 # force
        self._curr_passenger_count = 6 # passenger count currently on the train including crew
        self._max_passenger_count = 222 # combine max standing & seating passengers from data sheet
        self._prev_passenger_count = 0 # previous passenger count for the train
        self._passenger_mass = 0.0 # mass of the passengers on the train
        self._train_mass = 40900.0 # mass of the train empty from data sheet
        self._total_mass = 0.0 # total mass of the train with passengers
        self._temp_sp = 0.0 # internal temperature set point
        self._temperature = 0.0 # internal temperature of the train
        self._local_time = 0
        self._time = time.time()
        self._current_time = self._time
        self._prev_time = self._time
        self._block = 0 # current block the train is on
        self._beacon = "" # beacon information
        self._line = "BLUE" # line the train is on
        self._cmd_speed = 0.0 # commanded speed
        self._acceleration = 0.0 # acceleration of the train
        self._actual_velocity = 0.0 # actual velocity of the train
        self._authority = 0.0 # authority of the train
        self._speed_limit = 0.0 # speed limit of the train
        self._accel_limit = 0.5 # m/s^2 from data sheet
        self._decel_limit = -1.2 # m/s^2 from data sheet
        self._ebrake_decel_limit = -2.73 # m/s^2 from data sheet
        self._gravity = 9.81 # m/s^2
        self._grade = 0.0 # grade of the track
        self._elevation = 0.0 # elevation of the track
        self._underground = False # underground or above ground
        self._station_side = "" # station side the train is on
        self._ad_poll_attempts = 0 # number of attempts to poll for an advertisement
        self._ad_poll_rate = 5000 # milliseconds between advertisement changes
        self._dir_path = os.path.dirname(os.path.realpath(__file__))
        self._image_files = [
            self._dir_path + "/tropicana.jpg",
            self._dir_path + "/coca_cola.jpg",
            self._dir_path + "/pitt_logo.jpg",
            self._dir_path + "/station_ad.jpg",
            self._dir_path + "/jazz_train.png",
            self._dir_path + "/breath.jpg",
            self._dir_path + "/sweet_tooth.jpg",
            self._dir_path + "/eyes.jpg",
            ]
        self._current_ad = self._image_files[0]

        # -- Failure Modes -- #
        self._ebrake_failure = False # ebrake failure
        self._engine_failure = False # train engine failure
        self._sbrake_failure = False # service brake failure
        self._signal_failure = False # signal pickup failure

        # -- Controls -- #
        self._right_door = False # right door
        self._left_door = False # left door
        self._doors = False # either door
        self._int_lights = False # internal lights
        self._ext_lights = False # external lights
        self._emergency_brake = False  # emergency brake
        self._service_brake = False # service brake

        # -- Get Data from Other Modules -- #
        # TODO: change _train_ctrl_signals to _train_ctrl_signals from train controller signals
        self._train_ctrl_signals = None # train controller signals
        # TODO: change _track_model_signals to _track_model_signals from track model signals
        self._track_model_signals = None # track model signals

        # -- Run the Update Function -- #
        self.update()

    def update(self, thread=False):
        ##################################
        # Input Train Controller Signals #
        ##################################
        # Commanded Power
        # TODO: change get_cmd_power to get_cmd_power from train controller signals
        self.set_cmd_power(float(self.get_cmd_power()))  # Pass input from test UI text box

        # Internal Temperature
        # TODO: get temperature from train controller
        self.set_temperature(self.get_temperature())

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
        self.set_time()

        # Beacon
        # TODO: change get_beacon to get_beacon from track model signals
        self.set_beacon(self.get_beacon())

        # Line
        # TODO: change get_line to get_line from track model signals
        self.set_line(self.get_line())

        # Station Side
        # TODO: change get_station_side to get_station_side from track model signals
        self.set_station_side(self.get_station_side())

        # Block
        # TODO: change get_block to get_block from track model signals
        self.set_block(self.get_block())

        # Authority
        # TODO: change get_authority to get_authority from track model signals
        self.set_authority(float(self.get_authority()))

        # Speed Limit
        # TODO: change get_speed_limit to get_speed_limit from track model signals
        self.set_speed_limit(float(self.get_speed_limit()))

        # Elevation
        # TODO: change get_elevation to get_elevation from track model signals
        self.set_elevation(float(self.get_elevation()))

        # Grade
        # TODO: change get_grade to get_grade from track model signals
        self.set_grade(float(self.get_grade()))

        # Underground
        # TODO: change get_underground to get_underground from track model signals
        self.set_underground(bool(self.get_underground()))

        # Commanded Speed
        # TODO: change get_cmd_speed to get_cmd_speed from track model signals
        self.set_cmd_speed(float(self.get_cmd_speed()))

        ##############################
        # Output to Train Controller #
        ##############################
        # TODO: Add output to train controller

        #########################
        # Output to Track Model #
        #########################
        # TODO: Add output to track model

        #####################################
        # Internal Train Model Calculations #
        #####################################
        # Force
        self.set_force(float(self.get_force()))  # Pass input from test UI text box

        # Passenger Mass
        self.set_passenger_mass(self.get_curr_passenger_count())

        # Total Mass
        self.set_total_mass()

        # Force
        self.calc_force()

        # Acceleration
        self.calc_acceleration()

        # Actual Velocity
        self.calc_actual_velocity()

        # Enable Threading
        if thread:
            threading.Timer(0.1, self.update).start()

    # -- Simulation -- #
    # TODO: Remove Simulate Function during integration
    def beacon_simulate(self):
        if self._line == "":
            self.set_line("BLUE")
        if self._line.lower() == "green":
            # Set:
            # Station Name (Beacon)
            self.set_beacon("PIONEER")
            # print(self.get_beacon())  # TODO: Remove print statement
            # Authority
            self.set_authority(700)
            # Speed Limit
            self.set_speed_limit(45)
            # Elevation
            self.set_elevation(1)
            # Grade
            self.set_grade(0.01)
            # Underground
            self.set_underground(False)
            # Occupancy (Block)
            self.set_block(2)
        if self._line.lower() == "red":
            # Set:
            # Station Name (Beacon)
            self.set_beacon("SHADYSIDE")
            # print(self.get_beacon()) # TODO: Remove print statement
            # Authority
            self.set_authority(615)
            # Speed Limit
            self.set_speed_limit(40)
            # Elevation
            self.set_elevation(0.38)
            # Grade
            self.set_grade(0.005)
            # Underground
            self.set_underground(False)
            # Occupancy (Block)
            self.set_block(7)
        if self._line.lower() == "blue":
            # Set:
            # Station Name (Beacon)
            self.set_beacon("Station B")
            # print(self.get_beacon()) # TODO: Remove print statement
            # Authority
            self.set_authority(250)
            # Speed Limit
            self.set_speed_limit(50)
            # Elevation
            self.set_elevation(0.0)
            # Grade
            self.set_grade(0.0)
            # Underground
            self.set_underground(True)
            # Occupancy (Block)
            self.set_block(10)

    # -- Getters and Setters -- #
    def get_advertisement(self):
        # Choose a random image file from the list
        if self._ad_poll_attempts < self._ad_poll_rate:
            self._ad_poll_attempts += 100
            return self._current_ad
        else:
            self._ad_poll_attempts = 0
            self._current_ad = random.choice(self._image_files)
            return self._current_ad

    # acceleration
    def set_acceleration(self, _acceleration: float):
        self._acceleration = _acceleration

    def get_acceleration(self) -> float:
        return self._acceleration

    def calc_acceleration(self):
        # calc based on force and mass (Newton's Laws)
        self.set_acceleration(self.get_force() / self.get_total_mass())
        # max limit
        if self.get_acceleration() > self._accel_limit:
            self.set_acceleration(self._accel_limit)
        # ebrake min limit
        if self.get_acceleration() < self._ebrake_decel_limit:
            self.set_acceleration(self._ebrake_decel_limit)
        # sbrake min limit
        if self._ebrake_decel_limit < self.get_acceleration() < self._decel_limit:
            self.set_acceleration(self._decel_limit)
        # faults
        if (self.get_engine_failure() or self.get_signal_failure() or self.get_ebrake_failure() or self.get_sbrake_failure()) and self.get_actual_velocity() == 0:
            self.set_acceleration(0)
        # service brake or emergency brake
        if (self.get_service_brake() or self.get_emergency_brake()) and self.get_actual_velocity() == 0:
            self.set_acceleration(0)

        self.set_acceleration(self.get_acceleration())

    # station side
    def set_station_side(self, _station_side: str):
        self._station_side = _station_side

    def get_station_side(self) -> str:
        return self._station_side

    # authority
    def set_authority(self, _authority: float):
        self._authority = _authority

    def get_authority(self) -> float:
        return self._authority

    # speed limit
    def set_speed_limit(self, _speed_limit: float):
        self._speed_limit = _speed_limit

    def get_speed_limit(self) -> float:
        return self._speed_limit

    # elevation
    def set_elevation(self, _elevation: float):
        self._elevation = _elevation

    def get_elevation(self) -> float:
        return self._elevation

    # grade
    def set_grade(self, _grade: float):
        self._grade = _grade

    def get_grade(self) -> float:
        return self._grade

    # underground
    def set_underground(self, _underground: bool):
        self._underground = _underground

        # Set lights to bool of underground
        self.set_ext_lights(_underground)
        self.set_int_lights(_underground)

    def get_underground(self) -> bool:
        return self._underground

    # commanded speed
    def set_cmd_speed(self, _cmd_speed: float):
        self._cmd_speed = _cmd_speed

    def get_cmd_speed(self) -> float:
        return self._cmd_speed

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
    # TODO: Get time from track model
    # def set_time(self, _time: list):
    #     self._time = _time
    def set_time(self):
        self._time = time.time()

    def get_time(self) -> float:
        return self._time

    # temperature
    def set_temperature(self, temp:float):
        if self._temp_sp != temp:
            self._local_time = self._time
            self._temp_sp = temp
        self._temperature= round(self._temp_sp * (1 - math.exp(-(self._time - self._local_time))), 0)

    def get_temperature(self) -> float:
        return self._temperature

    # commanded power
    def set_cmd_power(self, _cmd_power: float):
        self._cmd_power = _cmd_power

    def get_cmd_power(self) -> float:
        return self._cmd_power

    # actual velocity
    def set_actual_velocity(self, _actual_velocity: float):
        self._actual_velocity = _actual_velocity

    def get_actual_velocity(self) -> float:
        return self._actual_velocity

    def calc_actual_velocity(self):
        # v = integrate acceleration over time
        # calculating dt
        self._current_time = self._time
        self.set_time()
        dt = self._current_time - self._prev_time
        # check if time difference is less than zero
        if dt < 0:
            return 0
        # calculate actual velocity according to change in acceleration over time
        self.set_actual_velocity(self.get_actual_velocity() + self.get_acceleration() * dt)
        self._prev_time =  self._current_time
        if self.get_acceleration() < 0.0 and self.get_actual_velocity() < 0.0:
            self.set_actual_velocity(0)

    # force
    def set_force(self, _force: float):
        self._force = _force

    def get_force(self) -> float:
        return self._force

    # TODO: Why does velocity not increase when grade and elevation are 0?
    def calc_force(self):
        # Max power limit
        if self.get_cmd_power() > self._max_power:
            self.set_force(self.get_total_mass() * self._accel_limit * self._friction_coeff)
        # Flat track
        if self.get_grade() == 0.0 and self.get_elevation() == 0.0:
            # Train not moving
            if self.get_actual_velocity() == 0:
                # commanded power is < 0 therefore train is braking
                if self.get_cmd_power() < 0:
                    # TODO: Determine if we need _decel_limit or _ebrake_decel_limit
                    self.set_force(self.get_total_mass() * self._decel_limit * self._friction_coeff)
                # commanded power is > 0 therefore train is accelerating
                elif self.get_cmd_power() > 0:
                    self.set_force(self.get_total_mass() * self._accel_limit * self._friction_coeff)
            # Train is moving
            else:
                self.set_force(abs(self.get_cmd_power() / self.get_actual_velocity()) - self._friction_coeff * self.get_total_mass())
        # Track is not flat
        else:
            # Calculate theta (angle of track)
            theta = math.atan(self.get_grade())
            mg_sin_theta = self.get_total_mass() * self._gravity * math.sin(theta * (3.14/180)) # Radians (pi/180)
            mg_cos_theta = self.get_total_mass() * self._gravity * math.cos(theta * (3.14/180))
            net_force = mg_sin_theta - self._friction_coeff * mg_cos_theta
            # Train not moving
            if self.get_actual_velocity() == 0:
                # commanded power is < 0 therefore train is braking
                if self.get_cmd_power() < 0:
                    self.set_force(net_force + self.get_total_mass() * self._decel_limit)
                # commanded power is > 0 therefore train is accelerating
                elif self.get_cmd_power() > 0:
                    self.set_force(self.get_cmd_power() - net_force)
            # Train is moving
            else:
                self.set_force(self.get_cmd_power() / self.get_actual_velocity() - net_force)
        # Service Brakes are Pulled
        if self.get_service_brake():
            self.set_force(self.get_force() + self.get_total_mass() * self._decel_limit)
        # Emergency Brakes or Failures
        elif self.get_emergency_brake() or self.get_engine_failure() or self.get_ebrake_failure() or self.get_sbrake_failure() or self.get_signal_failure():
            self.set_force(self.get_force() + self.get_total_mass() * self._ebrake_decel_limit)

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