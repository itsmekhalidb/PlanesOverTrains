# -- Imports -- #
import os
import math
import random
import time
import random as rand
import numpy as np
import threading

from api.train_model_train_controller_api import TrainModelTrainControllerAPI
from api.track_model_train_model_api import TrackModelTrainModelAPI

class TrainModel(object):
    def __init__(self, train_signals: TrainModelTrainControllerAPI, track_signals: TrackModelTrainModelAPI):

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
        self._time = 0 # time object set to midnight
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
        self._pass_emergency_brake = False # passenger emergency brake
        self._tc_wait = False # wait for train controller to release emergency brake
        self._service_brake = False # service brake
        self._service_brake_value = 0.0 # % service brake

        # -- Get Data from Other Modules -- #
        self._train_ctrl_signals = train_signals # train controller api
        self._track_model_signals = track_signals # track model api

        # -- Run the Update Function -- #
        self.update()

    def update(self, thread=False):
        #####################################
        # Internal Train Model Calculations #
        #####################################
        # Force
        self.set_force(float(self.get_force()))

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

        ##################################
        # Input Train Controller Signals #
        ##################################
        ## Failures
        # E-Brake Failure
        self._train_ctrl_signals.ebrake_failure = self.get_ebrake_failure()

        # Train Engine Failure
        self._train_ctrl_signals.engine_failure = self.get_engine_failure()

        # Service Brake Failure
        self._train_ctrl_signals.brake_failure = self.get_sbrake_failure()

        # Signal Pickup Failure
        self._train_ctrl_signals.signal_pickup_failure = self.get_signal_failure()

        ## Controls
        # Commanded Power
        self.set_cmd_power(self._train_ctrl_signals.cmd_power)

        # Internal Temperature
        self.set_temperature(self._train_ctrl_signals.temp_sp)

        # Right Door
        self.set_right_door(self._train_ctrl_signals.right_doors)

        # Left Door
        self.set_left_door(self._train_ctrl_signals.left_doors)

        # Internal Lights
        self.set_int_lights(self._train_ctrl_signals.int_lights)

        # External Lights
        self.set_ext_lights(self._train_ctrl_signals.ext_lights)

        # Emergency Brake
        self.set_emergency_brake(self._train_ctrl_signals.emergency_brake, tc_call=True)

        # Service Brake
        self.set_service_brake(self._train_ctrl_signals.service_brake_value > 0)

        # Service Brake Value
        self.set_service_brake_value(self._train_ctrl_signals.service_brake_value)

        ##############################
        # Output to Train Controller #
        ##############################
        # Train Line
        self._train_ctrl_signals.line = self.get_line()

        # Beacon
        self._train_ctrl_signals.beacon = self.get_beacon()

        # Authority
        self._train_ctrl_signals.authority = self.get_authority()

        # Commanded Speed
        self._train_ctrl_signals.cmd_speed = self.get_cmd_speed()

        # Speed Limit
        self._train_ctrl_signals.speed_limit = self.get_speed_limit()

        # Underground
        self._train_ctrl_signals.underground = self.get_underground()

        # Station Side
        self._train_ctrl_signals.station_side = self.get_station_side()

        # Time
        self._train_ctrl_signals.time = self.get_time()

        # Actual Velocity
        self._train_ctrl_signals.actual_velocity = self.get_actual_velocity()

        # Temperature
        self._train_ctrl_signals.temperature = self.get_temperature()

        # Passenger Ebrake
        self._train_ctrl_signals.passenger_emergency_brake = self.get_pass_emergency_brake()

        #############################
        # Input Track Model Signals #
        #############################
        # Passenger Onboard
        self.set_curr_passenger_count(self._track_model_signals.passenger_onboard)

        # Line
        self.set_line(self._track_model_signals.line)

        # Authority
        self.set_authority(self._track_model_signals.authority)

        # Commanded Speed
        self.set_cmd_speed(self._track_model_signals.cmd_speed)

        # Block
        self.set_block(self._track_model_signals.current_block)

        # Time
        self.set_time(self._track_model_signals.time)

        # Track Info
        self.set_track_info(self._track_model_signals.track_info)

        #########################
        # Output to Track Model #
        #########################
        # Passenger Update
        if self.get_beacon() != "": # We are at a station
            self.set_prev_passenger_count(self.get_curr_passenger_count())
        else:
            self.set_prev_passenger_count(0)

        # Send Passengers Departing when at a stop
        if not self.get_doors() and (self.get_left_door() or self.get_right_door()):
            self.set_doors(not self.get_doors()) # Open the doors
            if self.get_prev_passenger_count() > 0:
                # Depart all passengers at last stop before yard
                if (self.get_line().lower() == "green" and self.get_block() == 56) or (self.get_line().lower() == "red" and self.get_block() == 16):
                    self._track_model_signals.passenger_onboard = 0
                    self._track_model_signals.passenger_departing = self.get_prev_passenger_count()
                # Pick a random number of passengers to depart and onboard
                else:
                    self._track_model_signals.passenger_onboard = random.randint(0, self.get_curr_passenger_count())
                    self._track_model_signals.passenger_departing = random.randint(0, self.get_curr_passenger_count())
            else:
                # No passengers to depart
                self._track_model_signals.passenger_onboard = self.get_curr_passenger_count()
                self._track_model_signals.passenger_departing = 0
        elif self.get_doors() and not (self.get_left_door() or self.get_right_door()):
            self.set_doors(not self.get_doors()) # Close the doors

        # Actual Velocity
        self._track_model_signals.actual_velocity = self.get_actual_velocity()

        # Signal Pickup Failure
        self._track_model_signals.signal_pickup_failure = self.get_signal_failure()

        # Enable Threading
        if thread:
            threading.Timer(0.1, self.update).start()

    # -- Getters and Setters -- #
    def set_track_info(self, _track_info):
        # Check if the info exists
        if _track_info is not None and _track_info.get_block_info(self.get_line(),self.get_block()) is not None:
            # Get the info for the block
            info = _track_info.get_block_info(self.get_line(),self.get_block())

            # Beacon
            if info["beacon"] != "nan":
                self.set_beacon(str(info["beacon"])[9:])
            else:
                self.set_beacon("")
            # Speed Limit
            self.set_speed_limit(float(info["speed limit"]))
            # Elevation
            self.set_elevation(float(info["elevation"]))
            # Grade
            self.set_grade(float(info["grade"]))
            # Underground
            self.set_underground(bool(info["underground"]))
            # Station Side
            # TODO: Uncomment when station side is added to excel
            # self.set_station_side(info["station side"])

    def set_service_brake_value(self, _service_brake_value: float):
        self._service_brake_value = _service_brake_value

    def get_service_brake_value(self) -> float:
        return self._service_brake_value

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
        if self._ebrake_decel_limit < self.get_acceleration() < (self._decel_limit * self.get_service_brake_value()):
            self.set_acceleration(self._decel_limit * self.get_service_brake_value())
        # # faults
        # if (self.get_engine_failure() or self.get_signal_failure() or self.get_ebrake_failure() or self.get_sbrake_failure()) and self.get_actual_velocity() == 0:
        #     self.set_acceleration(0)
        # # emergency brake
        # if self.get_emergency_brake() and self.get_actual_velocity() != 0:
        #     self.set_acceleration(self._ebrake_decel_limit)
        return round(self.get_acceleration(), 3)

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
    def set_time(self, _time: int):
        self._time = _time

    def get_time(self) -> int:
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
        self._current_time = self.get_time()
        dt = self._current_time - self._prev_time
        self._prev_time = self._current_time
        # check if time difference is less than zero
        if dt < 0:
            return 0
        # calculate actual velocity according to change in acceleration over time
        self.set_actual_velocity(self.get_actual_velocity() + self.get_acceleration() * dt)
        if self.get_acceleration() < 0.0 and self.get_actual_velocity() < 0.0:
            self.set_actual_velocity(0)
        return self.get_actual_velocity()

    # force
    def set_force(self, _force: float):
        self._force = _force

    def get_force(self) -> float:
        return self._force

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
                    self.set_force(self.get_total_mass() * self._decel_limit * self.get_service_brake_value() * self._friction_coeff)
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
                    self.set_force(net_force + self.get_total_mass() * self._decel_limit * self.get_service_brake_value())
                # commanded power is > 0 therefore train is accelerating
                elif self.get_cmd_power() > 0:
                    self.set_force(self.get_cmd_power() - net_force)
            # Train is moving
            else:
                self.set_force(self.get_cmd_power() / self.get_actual_velocity() - net_force)
        # Service Brakes are Pulled
        if self.get_service_brake():
            self.set_force(self.get_force() + self.get_total_mass() * self._decel_limit * self.get_service_brake_value())
        # Emergency Brakes or Failures
        elif self.get_engine_failure() or self.get_emergency_brake() or self.get_signal_failure() or self.get_sbrake_failure():
            self.set_force(self.get_force() + self.get_total_mass() * self._ebrake_decel_limit)
        elif self.get_ebrake_failure():
            self.set_force(0)
        return round(self.get_force(),1)
    # passenger count
    def set_curr_passenger_count(self, _curr_passenger_count: int):
        self._curr_passenger_count = _curr_passenger_count
        self.set_passenger_mass(_curr_passenger_count)  # update mass each time passenger count changes

    def get_curr_passenger_count(self) -> int:
        return self._curr_passenger_count

    def set_prev_passenger_count(self, _prev_passenger_count: int):
        self._prev_passenger_count = _prev_passenger_count

    def get_prev_passenger_count(self) -> int:
        return self._prev_passenger_count

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

    # doors
    def set_doors(self, _doors: bool):
        self._doors = _doors

    def get_doors(self) -> bool:
        return self._doors

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

    # emergency brakes
    def set_pass_emergency_brake(self, _pass_emergency_brake: bool):
        self._pass_emergency_brake = _pass_emergency_brake

    def get_pass_emergency_brake(self) -> bool:
        return self._pass_emergency_brake
    def set_emergency_brake(self, emergency_brake_signal: bool, set_tc_wait: bool = False, tc_call=False):
        """
        Set the state of the emergency brake and optionally set the tc_wait flag.

        :param emergency_brake_signal: Boolean indicating whether the emergency brake is engaged.
        :param set_tc_wait: Boolean indicating whether to set the tc_wait flag.
        :param tc_call: Boolean indicating if the function is called from the train controller.
        """
        if not tc_call:
            # If called from UI or elsewhere, and Train Controller is not waiting, update the emergency brake
            if not self._tc_wait:
                self._emergency_brake = emergency_brake_signal
                if set_tc_wait:
                    self._tc_wait = True
            else:
                print("Train Controller is waiting. Cannot release emergency brake.")
        else:
            # If called from train controller, check if it's safe to release the emergency brake
            if not self._tc_wait or set_tc_wait:
                # Train controller is not waiting or we want to set tc_wait; it's safe to update the emergency brake
                self._emergency_brake = emergency_brake_signal
                self._tc_wait = set_tc_wait
            else:
                # Train controller is waiting; do not update the emergency brake
                print("Train Controller is waiting. Cannot release emergency brake.")

    def get_emergency_brake(self) -> bool:
        return self._emergency_brake

    # service brake
    def set_service_brake(self, _service_brake: bool):
        self._service_brake = _service_brake

    def get_service_brake(self) -> bool:
        return self._service_brake

    def launch_tm_ui(self):
        print("Launching Train Model UI")
        from train_model.Train_Model_UI import Ui_TrainModel_MainUI
        self._ui = Ui_TrainModel_MainUI(self)