#Imports
import math
import time
import random as rand
import numpy as np
import threading
import pandas as pd

class TrackModel(object):
    def __init__(self):
        #--Track Model Variables--

        self._switch_position = False #if train is switching tracks
        self._light_colors = "" #color of signal lights
        self._authority = 0 #how far train is permitted to travel
        self._gate_control = False #controls railway crossing gate
        self._commanded_speed = 0.0 #speed commanded by CTC
        self._railway_xing_lights = False #lights for railway crossing
        self._railway_xing = False #is the train at a railway crossing
        self._actual_velocity = 0.0 #how fast train is actually going
        self._offboarding = 0 #number of passengers offboarding
        self._current_block = 0 #block number on the track
        self._train_line = "" #color of the current line
        self._speed_limit = 0.0 #speed limit set by track model
        self._beacon = "" #static info on either side of station
        self._elevation = 0.0 #feet above ground level
        self._grade = 0.0 #slope of the track
        self._underground = False #if that section of track is underground
        self._onboarding = 0 #number of passengers boarding train
        self._occupancy = False #if block is occupied or not
        self._track_layout = "" #layout of the track

        #Failures
        self._broken_rail = False #broken rail failure
        self._circuit_failure = False #circuit failure
        self._power_failure = False #power failure
        self._train_engine_failure = False #train engine failure
        self._brake_failure = False #brake failure

        #Controls
        self._temperature = 0 #temperature of cabin

        #Data from Other Modules
        self._train_model_signals = None #signals from Train Model
        self ._track_controller_signals = None #signals from track controller

        self.update()

    def update(self, thread=False):
        #---- Failure Modes ----#

        #broken rail failure
        self.set_broken_rail(bool(self.get_broken_rail()))

        #circuit failure
        self.set_circuit_failure(bool(self.get_circuit_failure()))

        #power failure
        self.set_power_failure(bool(self.get_power_failure()))

        #engine failure
        self.set_engine_failure(bool(self.get_engine_failure()))

        #brake failure
        self.brake_failure(bool(self.get_brake_failure()))

        #---- Inputs from Track Controller ----#

        #switch position
        self.set_switch_position(self.get_switch_position())

        #light colors
        self.set_light_colors(self.get_light_colors())

        #authority
        self.set_authority(self.get_authority())

        #gate control
        self.set_gate_control(self.get_gate_control())

        #commanded speed
        self.set_commanded_speed(self.get_commanded_speed())

        #railway xing lights
        self.set_railway_xing_lights(self.get_railway_xing_lights())

        #---- Inputs from Train Model ----#

        #actual velocity
        self.set_actual_velocity(self.get_actual_velocity())

        #offboarding
        self.set_offboarding(self.get_offboarding())

        #---- Temperature Control ----#
        self.set_temperature(int(self.get_temperature()))

        #---- Outputs ----#
        #speed limit
        self.set_speed_limit(self.get_speed_limit())

        #current block
        self.set_current_block(self.get_current_block())

        #train line
        self.set_train_line(self.get_train_line())

        #beacon
        self.set_beacon(self.get_beacon())

        #elevation
        self.set_elevation(self.get_elevation())

        #grade
        self.set_grade(self.get_grade())

        #underground
        self.set_underground(self.get_underground())

        #onboarding
        self.set_onboarding(self.get_onboarding())

        #railway xing
        self.set_railway_xing(self.get_railway_xing())

        #occupancy
        self.set_occupancy(self.get_occupancy())

        #track layout
        self.set_track_layout(self.get_track_layout())

        #Enable threading
        if thread:
            threading.Timer(0.1, self.update).start()

        def beacon_simulate(self):
            if self.line == "":
                self.set_line("BLUE")
            if self.line.lower() == "green":        #---- GREEN LINE ----#
                self.set_beacon("PIONEER")          #Beacon
                self.set_authority(700)             #Authority
                self.set_speed_limit(45)            #Speed Limit
                self.set_elevation(1)               #Elevation
                self.set_grade(0.01)                #Grade
                self.set_underground(False)         #Underground
                self.set_current_block(2)           #Block Number
                self.set_occupancy(False)           #Occupancy

            if self.line.lower() == "red":          #---- RED LINE ----#
                self.set_beacon("SHADYSIDE")        #Beacon
                self.set_authority(615)             #Authority
                self.set_speed_limit(40)            #Speed Limit
                self.set_elevation(0.38)            #Elevation
                self.set_grade(0.005)               #Grade
                self.set_underground(False)         #Underground
                self.set_current_block(7)           #Block Number
                self.set_occupancy(False)           #Occupancy

            if self.line.lower() == "blue":         #---- BLUE LINE ----#
                self.set_beacon("Station B")        #Beacon
                self.set_authority(250)             #Authority
                self.set_speed_limit(50)            #Speed Limit
                self.set_elevation(0.0)             #Elevation
                self.set_underground(True)          #Underground
                self.set_current_block(10)          #Block Number
                self.set_occupancy(False)           #Occupancy

    #---- Getters & Setters ----#

    #Authority
    def set_authority(self, _authority: float):
        self._authority = _authority
    def get_authority(self) -> float:
        return self._authority

    #Speed Limit
    def set_speed_limit(self, _speed_limit: float):
        self._speed_limit = _speed_limit

    def get_speed_limit(self) -> float:
        return self._speed_limit

    #Switch Position
    def set_switch_position(self, _switch_position: bool):
        self._switch_position = _switch_position

    def get_switch_position(self) -> bool:
        return self._switch_position

    #Light Colors
    def set_light_colors(self, _light_colors: str):
        self._light_colors = _light_colors

    def get_light_colors(self) -> str:
        return self._light_colors

    #Gate Control
    def set_gate_control(self, _gate_control: bool):
        self._gate_control = _gate_control

    def get_gate_control(self) -> bool:
        return self._gate_control

    #Commanded Speed
    def set_commanded_speed(self, _commanded_speed: float):
        self._commanded_speed = _commanded_speed

    def get_commanded_speed(self) -> float:
        return self._commanded_speed

    #Railway Xing Lights
    def set_railway_xing_lights(self, _railway_xing_lights: bool):
        self._railway_xing_lights = _railway_xing_lights

    def get_railway_xing_lights(self) -> bool:
        return self._railway_xing_lights

    #Railway Xing
    def set_railway_xing(self, _railway_xing: bool):
        self._railway_xing = _railway_xing

    def get_railway_xing(self) -> bool:
        return self._railway_xing

    #Actual Velocity
    def set_actual_velocity(self, _actual_velocity: float):
        self._actual_velocity = _actual_velocity

    def get_actual_velocity(self) -> float:
        return self._actual_velocity

    #Offboarding
    def set_offboarding(self, _offboarding: int):
        self._offboarding = _offboarding

    def get_offboarding(self) -> int:
        return self._offboarding

    #Current Block
    def set_current_block(self, _current_block: int):
        self._current_block = _current_block

    def get_current_block(self) -> int:
        return self._current_block

    #Train Line
    def set_train_line(self, _train_line: str):
        self._train_line = _train_line

    def get_train_line(self) -> str:
        return self._train_line

    #Speed Limit
    def set_speed_limit(self, _speed_limit: float):
        self._speed_limit = _speed_limit

    def get_speed_limit(self) -> float:
        return self._speed_limit

    #Beacon
    def set_beacon(self, _beacon: str):
        self._beacon = _beacon

    def get_beacon(self) -> str:
        return self._beacon

    #Elevation
    def set_elevation(self, _elevation: float):
        self._elevation = _elevation

    def get_elevation(self) -> float:
        return self._elevation

    #Grade
    def set_grade(self, _grade: float):
        self._grade = _grade

    def get_grade(self) -> float:
        return self._grade

    #Underground
    def set_underground(self, _underground: bool):
        self._underground = _underground

    def get_underground(self) -> bool:
        return self._underground

    #Onboarding
    def set_onboarding(self, _onboarding: int):
        self._onboarding = _onboarding

    def get_onboarding(self) -> int:
        return self._onboarding

    #Occupancy
    def set_occupancy(self, _occupancy: bool):
        self._occupancy = _occupancy

    def get_occupancy(self) -> bool:
        return self._occupancy

    #Track Layout
    def set_track_layout(self, _track_layout: str):
        self._track_layout = _track_layout

    def get_track_layout(self) -> str:
        return self._track_layout

    #Broken Rail
    def set_broken_rail(self, _broken_rail: bool):
        self._broken_rail = _broken_rail

    def get_broken_rail(self) -> bool:
        return self._broken_rail

    #Circuit Failure
    def set_circuit_failure(self, _circuit_failure: bool):
        self._circuit_failure = _circuit_failure

    def get_circuit_failure(self) -> bool:
        return self._circuit_failure

    #Power Failure
    def set_power_failure(self, _power_failure: bool):
        self._power_failure = _power_failure

    def get_power_failure(self) -> bool:
        return self._power_failure

    #Train Engine Failure
    def set_train_engine_failure(self, _train_engine_failure: bool):
        self._train_engine_failure = _train_engine_failure

    def get_train_engine_failure(self) -> bool:
        return self._train_engine_failure

    #Brake Failure
    def set_brake_failure(self, _brake_failure: bool):
        self._brake_failure = _brake_failure

    def get_brake_failure(self) -> bool:
        return self._brake_failure







