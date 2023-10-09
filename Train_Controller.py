import threading
import math
import time
import numpy as np

class TrainController(object)
    def __int__(self):
        #priv variables
        self._current_velocity = 0
        self._maximum_velocity = 0
        self._power = 0
        self._engine_failure = False
        self._signal_pickup_failure = False
        self._service_brake_failure = False
        self._emergency_brake_failure = False
        self._underground_status = False #This is needed to determine if the lights must be on
        self._right_door_open = False
        self._left_door_open = False
        self._internal_lights_on = False
        self._external_lights_on = False
        self._kp = 0
        self._ki = 0
        self._ek = 0
        self._uk = 0
        self._beacon = 0

        # Update Function
        self.update()

    def update(self, thread=False):

        #call getters and setters
        # TODO: change this to get from either driver or train model
        # self.set_anything(self.get_anything)

    # put set and get functions here
    def set(self, var: int):
        var = var

    def get(self) -> int:
        return var

    def s