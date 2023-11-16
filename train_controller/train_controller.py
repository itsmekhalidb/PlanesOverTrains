import threading
import math
import time

import numpy as np
from api.train_model_train_controller_api import TrainModelTrainControllerAPI
from .Controller import Controller
from .Backup_Controller import Backup_Controller


KP = 8000
KI = 10
DWELL_TIME = 60
BRAKING_DIFFERENCE = 0.5
BACKUP_THRESHOLD = 2000
STOPPING_SPEED = 15
SLOWDOWN = .0124

NIGHT = 7
DAY = 7

TRAIN_MASS = 40900.0
SB_FORCE = TRAIN_MASS * 1.2
EB_FORCE = TRAIN_MASS * 2.73

class TrainController:

    # def __init__(self, train_model_api: TrainModelTrainControllerAPI):
    def __init__(self, train_model_api, test=False):

        #priv variables
        self._current_velocity = 0.0
        self._maximum_velocity = 0.0
        self._commanded_velocity = 0.0
        self._commanded_power = 0.0
        self._authority = 0.0
        self._setpoint_speed = 0.0
        self._engine_failure = False
        self._signal_pickup_failure = False
        self._service_brake_failure = False
        #self._service_brake_status = False
        self._service_brake_value = 0.0
        self._emergency_brake_failure = False
        self._emergency_brake_status = False
        self._underground_status = False
        # non-vital
        self._right_door_open = False
        self._left_door_open = False
        self._internal_lights_on = False
        self._external_lights_on = False
        self._auto_stat = False
        self._kp = 0.0
        self._ki = 0.0
        self._ek = 0.0
        self._uk = 0.0
        self._ti = 1.0
        self._beacon = 0
        self._previous_uk = 0.0
        self._previous_ek = 0.0
        self._train_line = ""
        self._prev_station = ""
        self._station = ""
        self._side = ""
        self._stop = False
        self._time = [0]
        self._temp_sp = 0.0 # internal temperature set point
        self._temperature = 0.0 # internal temperature of the train
        self._time = 0
        self._controller = Controller(self._time)
        self._backup_controller = Backup_Controller(self._time)
        self.set_gains(KP,KI)

        # Update Function
        self.train_model = train_model_api
        if not test:
            self.update()

    def update(self, thread=False):
        self.set_auto_status(bool(self.get_auto_status()))
        self.train_model.right_doors = self.get_right_door_status()
        self.train_model.left_doors = self.get_left_door_status()
        self.train_model.int_lights = self.get_internal_lights()
        self.train_model.ext_lights = self.get_external_lights()
        self.set_underground_status(self.train_model.underground)
        self.train_model.service_brake_value = self.get_service_brake_value()
        self.set_emergency_brake_status(self.train_model.passenger_emergency_brake or self.get_ebrake_status())
        self.train_model.emergency_brake = self.get_ebrake_status()
        #self.set_service_brake_status(bool(self.get_service_brake_status()))
        self.set_emergency_brake_failure(self.train_model.ebrake_failure)
        self.set_service_brake_failure(self.train_model.brake_failure)
        self.set_engine_status(self.train_model.engine_failure)
        self.set_signal_pickup_failure_status(self.train_model.signal_pickup_failure)
        self.train_model.cmd_speed = self.get_commanded_velocity()
        self.set_maximum_veloctity(self.train_model.speed_limit)
        self.set_current_velocity(self.train_model.actual_velocity)
        self.set_commanded_velocity(self.train_model.cmd_speed)
        self.set_authority(round(self.train_model.authority*3.28084,3))
        #self.set_current_velocity(float(self.train_model.actual_velocity))
        self.set_ki(float(self.get_ki()))
        self.set_kp(float(self.get_ki()))
        self.set_eK(float(self.get_commanded_velocity()), float(self.get_actual_velocity()))
        self.set_uk(float(self._ek))
        self.set_power()
        self.train_model.cmd_power = self.get_commanded_power()
        self.set_service_brake_value(float(self.get_service_brake_value()))
        self.train_model.temp_sp = self.get_temperature_sp()
        self.set_temperature(self.train_model.temperature)
        self.set_train_line(self.train_model.line)
        self.set_internal_lights()
        self.set_external_lights()
        self.set_setpoint_speed(self._setpoint_speed)
        self.set_beacon(self.train_model.beacon)
        self.set_time(self.train_model.time)

        if thread:
            threading.Timer(0.1, self.update).start()

    def set_next_station(self, station: str):
        self._next_station = station

    def set_temperature_sp(self, temp_sp: float):
        self._temp_sp = temp_sp

    def get_temperature_sp(self) -> float:
        return self._temp_sp

    def set_temperature(self, temp: float):
        self._temperature = temp

    def get_temperature(self) -> float:
        return self._temperature

    def set_beacon(self, beacon: str):
        self._beacon = beacon

    def set_station_status(self, status: str):
        self._station_status = status
    def set_engine_status(self, stat: bool):
        self._engine_failure = stat
    def set_auto_status(self, stat: bool):
        self._auto_stat = stat
    def set_maximum_veloctity(self, max_speed: float):
        self._maximum_velocity = max_speed
    def set_commanded_velocity(self, v: float):
        if v <= self._maximum_velocity:
            self._commanded_velocity = v
    def set_current_velocity(self, c : float):
        self._current_velocity = c

    def set_internal_lights(self):
        if not self.get_auto_status():
            if self._underground_status or self.get_time_of_day():
                self._internal_lights_on = True
            else:
                self._internal_lights_on = False

    def set_external_lights(self):
        if not self.get_auto_status():
            if self._underground_status or self.get_time_of_day():
                self._external_lights_on = True
            else:
                self._external_lights_on = False

    # def set_engine_failure_status(self, status: bool):
    #     self._engine_failure = status
    def set_signal_pickup_failure_status(self, status: bool):
        self._signal_pickup_failure = status
    def set_service_brake_value(self, value: float):
        if value != 0 :
            self._service_brake_value = value
        if self._service_brake_value < 0.19:
            self._service_brake_value = 0
    def set_emergency_brake_status(self, status: bool):
        self._emergency_brake_status = status
    def set_emergency_brake_failure(self, status: bool):
        self._emergency_brake_failure = status
    def set_kp(self, kp: float):
        # self._kp = 1/ki # check out formulas and clarify
        self._kp = kp
        # print("Kp = " + str(self._kp))
    def set_ki(self, ki:float):
        # self._ki = 1/self._ti
        self._ki = ki
        # print("Ki = " + str(self._ki))
    def set_uk(self, current_ek: float):
        self._uk = self._previous_uk + .5 * (current_ek + self._previous_ek)
        self._previous_uk = self._uk
    def set_eK(self, desired: int, actual: int):
        self._ek = self._commanded_velocity - self._current_velocity
        self._previous_ek = self._ek

    def update_stop(self):
        if (self.get_beacon()) != "" and not self._stop and self._prev_station!=self.get_beacon() and self.get_authority()<=0:
            self._stop = True
            self._stop_time = self.get_time()
            self.set_service_brake_value(1.0)

            self.set_station_side()

        if self._stop and self.get_time() >= self._stop_time + DWELL_TIME or self.get_auto_status():
            self._stop = False
            self.set_service_brake_value(0.0)
            self.set_right_door_status(False)
            self.set_left_door_status(False)

        self._prev_station = self.get_beacon()

    def set_power(self):
        #TODO: check if we are at a stop
        if not self.get_auto_status():
           self.update_stop()
        # Define function local vars
        backup_power = 0.0
        if self.get_signal_pickup_failure() or self.get_engine_status() or self.get_service_brake_failure_status():
            self._emergency_brake_status = True
        if not self.get_auto_status():
            speed = self._setpoint_speed #TODO: make spinbox in UI point to this var
        else:
            speed = self._commanded_velocity
        if self._authority <= 0 or self.get_emergency_brake_failure_status() or self.get_service_brake_value()>0:
            self._controller.update(self._current_velocity, 0.0)
            self._backup_controller.update(self._current_velocity, 0.0)
            power = 0.0
        else:
            power = self._controller.update(self._current_velocity, speed)
            backup_power = self._backup_controller.update(self._current_velocity, speed)
        if abs(power - backup_power)>2000:
            power = (power + backup_power)/2
        if power>0 and power<=120000:
            power = round(power,2)
        elif power>120000:
            power = 120000
        else:
            power = 0.0
        # TODO: Implement coming to a stop
        braking_distance_val = self.braking_distance(self.get_actual_velocity())
        ebrake_distance_val = self.ebrake_distance(self.get_actual_velocity())
        if self.get_actual_velocity()>speed+BRAKING_DIFFERENCE:
            self._decreasing_speed = True
        elif self.get_authority()<=0 and braking_distance_val > SLOWDOWN:
            self._emergency_decreasing_speed = True
        elif self.get_authority() < braking_distance_val:
            self._decreasing_speed = True
        else:
            self._decreasing_speed = False
            self._emergency_decreasing_speed = False
        self.get_service_brake_value()
        self._commanded_power = power if power < 120000 else 120000
        return power


    def set_setpoint_speed(self, speed: float):
        if speed <= self._maximum_velocity:
            self._setpoint_speed = speed
        else:
            self._setpoint_speed = self._maximum_velocity
    def set_right_door_status(self,stat: bool):
        self._right_door_open = stat
    def set_left_door_status(self, stat: bool):
        self._left_door_open = stat
    def set_underground_status(self, stat: bool):
        self._underground_status = stat
    def set_authority(self, a: float):
        self._authority = a
    def set_ebrake_failure(self, f: bool):
        self._emergency_brake_failure = f
    def set_service_brake_failure(self, stat: bool):
        self._service_brake_failure = stat
    def set_gains(self, kp: float, ki: float):
        self._controller.set_gains(kp, ki)
        self._backup_controller.set_gains(kp, ki)
    def set_train_line(self, line: str):
        self._train_line = line
    def set_time(self, time: int):
        self._time = time
    def get_current_velocity(self)->float:
        return self._current_velocity
    def get_auto_status(self)->bool:
        return self._auto_stat
    def get_maximum_velocity(self)->float:
        return self._maximum_velocity
    def get_kp(self) -> float:
        return self._controller._kp
    def get_ki(self)->float:
        return self._controller._ki
    def get_right_door_status(self)->bool:
        return self._right_door_open
    def get_left_door_status(self)->bool:
        return self._left_door_open
    def get_internal_lights(self)->bool:
        return self._internal_lights_on
    def get_external_lights(self)->bool:
        return self._external_lights_on
    def get_underground_status(self)->bool:
        return self._underground_status
    def get_ebrake_status(self)->bool:
        return self._emergency_brake_status
    def get_service_brake_value(self)->float:
        return self._service_brake_value
    def get_emergency_brake_failure_status(self)->bool:
        return self._emergency_brake_failure
    def get_service_brake_failure_status(self)->bool:
        return self._service_brake_failure
    def get_commanded_velocity(self)->float:
        return self._commanded_velocity
    def get_authority(self)->float:
        return self._authority
    def get_engine_status(self)->bool:
        return self._engine_failure
    def get_signal_pickup_failure(self)->bool:
        return self._signal_pickup_failure
    def get_actual_velocity(self)->float:
        return self._current_velocity
    def get_commanded_power(self)->float:
        return self._commanded_power
    def get_train_line(self)->str:
        return self._train_line

    def get_next_station(self)->str:
        return self._next_station

    def braking_distance(self, velocity: float)->float:
        return .000621371*(.5*TRAIN_MASS*(self._current_velocity*.44704)**2)/SB_FORCE

    def get_station_status(self)->str:
        return self._station_status

    def ebrake_distance(self, velocity: float)->float:
        return .000621371*(.5*TRAIN_MASS*(self._current_velocity*.44704)**2)/EB_FORCE

    def get_beacon(self)->str:
        return self._beacon

    def get_time(self)-> int:
        return self._time

    def get_time_of_day(self)->bool:
        hour = self.get_time()//3600
        return hour >= NIGHT + 12 or hour <= DAY

    def set_station_side(self):

        if self._side == "Left":
            self.set_left_door_status(True)
        elif self._side == "Right":
            self.set_right_door_status(True)
        elif self._side == "Left/Right":
            self.set_left_door_status(True)
            self.set_right_door_status(True)
        else:
            self.set_left_door_status(False)
            self.set_right_door_status(False)

    def get_side(self)->str:
        return self._side
    def set_side(self, side: str):
        self._side = side
    def get_setpoint_speed(self)->float:
        return self._setpoint_speed
    def launch_tc_ui(self):
        from train_controller.Train_Controller_Main_Window import Ui_MainWindow
        print("Launching Train Controller UI")
        self._ui = Ui_MainWindow(self)
