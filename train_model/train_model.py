# -- Imports -- #
import math
import random as rand
import numpy as np
import threading

class TrainModel(object):
    def __init__(self):

        # -- Train Model Variables -- #
        self._cmd_power = 0.0 # commanded power
        self._temp_sp = 0.0 # internal temperature set point
        self._temperature = 0.0 # internal temperature of the train
        self._local_time = 0
        self._time = 0

        # -- Run the Update Function -- #
        self.update()

    def update(self, thread=False):
        """
        Updates the train model
        Inputs: Train Controller, Track Model
        Outputs: Train Controller, Track Model
        """

        # Input Train Controller Signals
        self.set_cmd_power()

        # Input Track Model Signals

        # Output to Train Controller

        # Output to Track Model

        # Internal Train Model Calculations
        # Temperature
        self.set_temperature(self._temp_sp)

        # Enable Threading
        if thread:
            threading.Timer(0.1, self.update).start()

    def set_temperature(self, temp:float):
        """
        Sets the temperature of the train
        Inputs: Temperature Setpoint
        Outputs: Temperature
        """
        # Calculate the temperature
        if self._temp_sp != temp:
            self._local_time = self._time[0]
            self._temp_sp = temp
        self._temperature= round(self._temp_sp * (1 - math.exp(-(self._time[0] - self._local_time))), 0)
    def get_temperature(self):
        """
        Gets the temperature of the train
        Inputs: None
        Outputs: Temperature
        """
        return self._temperature