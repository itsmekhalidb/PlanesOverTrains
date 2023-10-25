import threading
import math
import time
import numpy as np

class TrainController:

    def __init__(self, train_model):
        #priv variables
        self._current_velocity = 0.0
        self._maximum_velocity = 0.0
        self._commanded_velocity = 0.0
        self._commanded_power = 0.0
        self._authority = 0.0
        self._engine_failure = False
        self._signal_pickup_failure = False
        self._service_brake_failure = False
        #self._service_brake_status = False
        self._service_brake_value = 0.0
        self._emergency_brake_failure = False
        self._emergency_brake_status = False
        self._underground_status = False
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
        self._next_station = ""
        self._station_status = ""
        self._temp_sp = 0.0 # internal temperature set point
        self._temperature = 0.0 # internal temperature of the train

        # Update Function
        self.train_model = train_model
        self.update()

    def update(self, thread=False):

        self.set_auto_status(bool(self.get_auto_status()))
        self.train_model.right_doors = self.get_right_door_status()
        self.train_model.left_doors = self.get_left_door_status()
        self.train_model.int_lights = self.get_internal_lights()
        self.train_model.ext_lights = self.get_external_lights()
        self.set_underground_status(self.train_model.underground)
        self.train_model.service_brake_value = self.get_service_brake_value()
        self.train_model.emergency_brake = self.get_ebrake_status()
        #self.set_service_brake_status(bool(self.get_service_brake_status()))
        self.set_emergency_brake_failure(self.train_model.ebrake_failure)
        self.set_service_brake_failure(self.train_model.brake_failure)
        self.set_engine_status(self.train_model.engine_failure)
        self.set_signal_pickup_failure_status(self.train_model.signal_pickup_failure)
        self.train_model.cmd_speed = self.get_commanded_velocity()
        self.set_maximum_veloctity(float(self.get_maximum_velocity()))
        self.set_current_velocity(self.train_model.actual_velocity)
        self.set_commanded_velocity(self.train_model.cmd_speed)
        self.set_authority(float(self.get_authority()))
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

    # TODO: Lights do not turn on if underground, needs fix
    def set_internal_lights(self, status: bool):
        if self._underground_status:
            self._internal_lights_on = True
        self._internal_lights_on = status
    def set_external_lights(self, status: bool):
        if self._underground_status:
            self._external_lights_on = True
        self._external_lights_on = status
    # def set_engine_failure_status(self, status: bool):
    #     self._engine_failure = status
    def set_signal_pickup_failure_status(self, status: bool):
        self._signal_pickup_failure = status
    def set_service_brake_value(self, value: float):
        self._service_brake_value = value
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

    # TODO: Desired power is not being passed in at any point in your code, needs fix
    def set_power(self):
        if self.get_service_brake_failure_status() or self.get_emergency_brake_failure_status() or self.get_signal_pickup_failure() or self.get_engine_status():
            self._commanded_power = 0
        elif (self._kp * self._ek + self._ki + self._uk) <= 120000:
            self._commanded_power = self._kp * self._ek + self._ki + self._uk
        else:
            self._commanded_power = 120000


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
    def set_train_line(self, line: str):
        self._train_line = line
    def get_current_velocity(self)->float:
        return self._current_velocity
    def get_auto_status(self)->bool:
        return self._auto_stat
    def get_maximum_velocity(self)->float:
        return self._maximum_velocity
    def get_kp(self) -> float:
        return self._kp
    def get_ki(self)->float:
        return self._ki
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

    def get_station_status(self)->str:
        return self._station_status

    def launch_tc_ui(self):
        from train_controller.Train_Controller_Main_Window import Ui_MainWindow
        print("Launching Train Controller UI")
        self._ui = Ui_MainWindow(self)
