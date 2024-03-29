#Imports
import datetime
from datetime import datetime
import math
import time
import random as rand
import numpy as np
import threading
import pandas as pd
from api.track_controller_track_model_api import TrackControllerTrackModelAPI
from api.track_model_train_model_api import TrackModelTrainModelAPI, Trainz
from api.ctc_track_model_api import CTCTrackModelAPI
import traceback
from track_model.block_info import block_info
from typing import DefaultDict


class TrackModel(object):
    def __init__(self, TrainModels: Trainz, trackCtrlSignal: TrackControllerTrackModelAPI, CTCSignal: CTCTrackModelAPI):
        #--Track Model Variables--

        self._switch_position = {} #if train is switching tracks
        self._light_colors = {} #color of signal lights
        self._authority = 0.0 #how far train is permitted to travel
        self._gate_control = False #controls railway crossing gate
        self._commanded_speed = 0.0 #speed commanded by CTC
        self._railway_xing_lights = False #lights for railway crossing
        self._railway_xing = False #is the train at a railway crossing
        self._actual_velocity = 0.0 #how fast train is actually going
        self._offboarding = 0 #number of passengers offboarding
        self._current_block = list() #block number on the track
        self._train_line = "" #color of the current line
        self._speed_limit = 0.0 #speed limit set by track model
        self._beacon = "" #static info on either side of station
        self._elevation = 0.0 #feet above ground level
        self._grade = 0.0 #slope of the track
        self._underground = False #if that section of track is underground
        self._onboarding = 0 #number of passengers boarding train
        self._occupancy = False #if block is occupied or not
        self._filepath = ""  # filepath to block info
        self._track_layout = block_info(self._filepath) #layout of the track
        self._temperature = 0
        self._track_layout_loaded = 0 #done for track layout
        self._block_length = 0.0 #block length
        self._local_time = 0
        self._time = time.time()
        self._dt = 0
        self._current_time = self._time
        self._prev_time = self._time
        self._train_models = TrainModels.train_apis # dictionary of train model apis
        self._train_ids = [] # list of train ids
        self._distance = 0.0
        self.tof = False
        self._direction = 1 #direction of travel (1=forward, 0=backward)
        self._switchionary = {}



        #Failures
        self._broken_rail = False #broken rail failure
        self._circuit_failure = False #circuit failure
        self._power_failure = False #power failure
        self._heater_failure = False

        #Controls
        self._temperature = 0 #temperature of cabin

        #Data from Other Modules
        self._track_controller_signals = trackCtrlSignal #api from track controller
        self._train_model_signals = self._track_controller_signals._train_out #dictionary of apis to train model
        self._ctc_signals = CTCSignal #api from ctc
        self._TrainModels = TrainModels #dictionary api


        self.update()

    def update(self, thread=True):
        #---- Failure Modes ----#
        #broken rail failure
        self.set_broken_rail(bool(self.get_broken_rail()))

        #circuit failure
        self.set_circuit_failure(bool(self.get_circuit_failure()))

        #power failure
        self.set_power_failure(bool(self.get_power_failure()))

        #track heater failure
        self.set_heater_failure(bool(self.get_heater_failure()))

        #---- Inputs from Track Controller ----#

        #switch position
        self.set_switch_position(self._track_controller_signals._switches)


        #light colors
        self.set_light_colors(self._track_controller_signals._lights)


        #authority
        # self.set_authority(self._track_controller_signals._authority)
        # self._train_models[1].authority = 10.0

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

        #block length
        self.set_block_length(self.get_block_length())

        #---- Internal Functions ----#
        #temperature
        self.set_temperature(int(self.get_temperature()))

        #track layout
        self.set_track_layout(self._filepath)
        self._track_controller_signals._filepath = self._filepath
        # self._train_models[1].track_info = self.get_track_layout()

        #---- Outputs ----#
        #speed limit
        self.set_speed_limit(self.get_speed_limit())

        #track layout
        self._track_controller_signals._track_info = self.get_track_layout()

        #current block occupancy list
        self._track_controller_signals._train_in = self._current_block
        # print("track model train in " + str(self._track_controller_signals._train_in))
        # get second element of each sublist in the list self._current_block
        self._track_controller_signals._occupancy = {"Green": [str(i[1]) for i in self._current_block if i[3] == 'green'],
                                                     "Red": [str(i[1]) for i in self._current_block if i[3] == 'red']}

        #print("track model train in " + str(self._track_controller_signals._train_in))

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

        #line
        self.set_line(self._track_controller_signals._line)
        # self._train_models[1].line = self.get_line()

        #dt
        if not isinstance(self._track_controller_signals._time, int):
            self.calc_dt(self._track_controller_signals._time.timestamp())

        # update train model signals
        self._train_model_signals = self._track_controller_signals._train_out #dictionary of apis to train model

        # Make a train dictionary out of the train ids and train lines
        # NOTE: you can make this self. if you want but not necessary
        train_dict = {train_id: train_line for train_id, train_line in zip(self._track_controller_signals._train_ids, self._track_controller_signals._train_lines)}

        for i in self._track_controller_signals._train_ids:
            index = int(i) - 1
            if index not in self._train_ids:
                self._train_ids.append(index)
                self._TrainModels.train_apis[index] = TrackModelTrainModelAPI()
                self._TrainModels.train_apis[index].line = train_dict[i]
                self._TrainModels.train_apis[index].current_block = 63 if train_dict[i].lower() == "green" else 9
                self._TrainModels.train_apis[index].direction = 1 if train_dict[i].lower() == "green" else -1
                self._TrainModels.train_apis[index].track_info = self.get_track_layout()
                self._ctc_signals._ticket_sales.append([index, self._TrainModels.train_apis[index].passenger_departing])
            self._TrainModels.train_apis[index].time = self._track_controller_signals._time.timestamp() #TODO: Change this to an internal function get_time()
            self._ctc_signals._ticket_sales[index][1] = self._TrainModels.train_apis[index].passenger_departing
            self.set_onboarding(self._TrainModels.train_apis[index].passenger_departing)
            self.set_offboarding(self._TrainModels.train_apis[index].passenger_onboard)
            try:
                self._TrainModels.train_apis[index].authority = self._train_model_signals[index+1][0]
                self._TrainModels.train_apis[index].cmd_speed = self._train_model_signals[index+1][1]
                #print("train model signals: " + str(self._train_model_signals[index+1]))
                #print("train " + str(index) + " authority = " + str(self._TrainModels.train_apis[index].authority))
            except Exception as e:
                print("waiting for departure... ")
            self._TrainModels.train_apis[index].cum_distance += self.update_traveled_distance(self._TrainModels.train_apis[index].actual_velocity)
            self._TrainModels.train_apis[index].current_block = self.update_current_block(self._TrainModels.train_apis[index])
            if index + 1 > len(self._current_block):
                self._current_block.append([self._TrainModels.train_apis[index].actual_velocity, self._TrainModels.train_apis[index].current_block, self._TrainModels.train_apis[index].cum_distance, self._TrainModels.train_apis[index].line])
            else:
                self._current_block[index] = [self._TrainModels.train_apis[index].actual_velocity, self._TrainModels.train_apis[index].current_block,  self._TrainModels.train_apis[index].cum_distance, self._TrainModels.train_apis[index].line]
            # print(self._current_block)


        #Enable threading
        if thread:
            threading.Timer(0.1, self.update).start()


    #---- Getters & Setters ----#
    def calc_dt(self, time):
        self._current_time = time
        self._dt = self._current_time - self._prev_time
        self._prev_time = self._current_time

    def update_traveled_distance(self, velocity):
        dist_traveled = velocity * self._dt
        return abs(dist_traveled)

    def update_current_block(self, train):
        # Only Load Track Model if filepath is not empty -- One Time
        if self._track_layout.get_filepath() != "":
            self._switchionary = self._track_layout.get_switchionary(train.line)
            self._switch_position = self._track_controller_signals._switches[(train.line).capitalize()]




        try:
            if train.current_block in self._switchionary.keys() and train.cum_distance > train.track_info.get_block_info(train.line, train.current_block)['length']:
                inc = self._switchionary[train.current_block][1]
                sw = self._switchionary[train.current_block][3]
                sw_label = self._switchionary[train.current_block][4]
                if train.current_block == 57 and train.direction == inc and self._switch_position[sw_label] == 1:
                    train.current_block = 151
                if train.current_block == 9 and train.direction != inc and self._switch_position[sw_label] == 1:
                    train.curr_block = 77
                if train.direction == inc and self._switch_position[sw_label] == sw:
                    # print(self._switchionary[train.current_block][0])
                    train.direction = self._switchionary[train.current_block][2]
                    self._direction = train.direction
                    train.current_block = self._switchionary[train.current_block][0]
                    train.cum_distance = 0

            if train.current_block is not None and train.cum_distance <= 0 or train.current_block != 151 or train.current_block != 9:
                if train.cum_distance > train.track_info.get_block_info(train.line, train.current_block)['length']:
                    train.cum_distance = 0
                    # print(train.current_block)
                    train.current_block += train.direction
                    # print(train.current_block)


                    # how to get switch position
                    # pos = self.get_switch_position(self._track_controller_signals._line.capitalize(), '63')) # returns 0 or 1

                    # how to set direction
                    # self._TrainModels.train_apis[index].direction = 0 or 1 # 1 is forward, 0 is backward


            return train.current_block
        except Exception as e:
            traceback.print_exc()
            print("You must upload the Track Model before dispatching a train")
            print(e)




    def get_occupancy(self):
        return self._current_block
    #Occupancy
    def set_current_block(self, _current_block: int):
        self._current_block.append(_current_block)

    def get_current_block(self) -> list:
        return self._current_block

    def get_direction(self) -> int:
        return self._direction



    #Line
    def set_line(self, _line: str):
        self._line = _line
    def get_line(self) -> str:
        return self._line

    def set_switch_to(self, _switch_to: {}):
        self._switch_to = _switch_to

    def get_switch_to(self) -> {}:
        return self._switch_to

    def set_block_length(self, _block_length: float):
        self._block_length = _block_length

    def get_block_length(self) -> float:
        return self._block_length

    #Filepath
    def set_filepath(self, _filepath: str):
        self._filepath = _filepath
    def get_filepath(self) -> str:
        return self._filepath

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
    def set_switch_position(self, _switch_position: {}):
        self._switch_position = _switch_position

    def get_switch_position(self, line, switch) -> int:
        try:
            return int(self._switch_position[str(line)][str(switch)])
        except KeyError:
            # Handle the case when the color or switch_number is not found
            print(f"Error: Color '{str(line)}' or switch number '{str(switch)}' not found.")

    #Light Colors
    def set_light_colors(self, _light_colors: {}):
        self._light_colors = _light_colors

    def get_light_colors(self) -> {}:
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

    def set_temperature(self, _temperature: int):
        self._temperature = _temperature

    def get_temperature(self) -> int:
        return self._temperature

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



    #get veolocity, multiple velocity & time to get distance, compare distance and block length, constantly add distance, dt could be 1 second,
    # def set_distance(self, _distance):

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
    def set_track_layout(self, path: str):
        if self._track_layout_loaded == 0 and self._filepath != "":
            self._track_layout = block_info(filepath=path)
            self._track_layout_loaded = 1
        else:
            self._track_layout = self.get_track_layout()

    def get_track_layout(self) -> block_info:
        if self._filepath == "":
            return {}
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
    def set_engine_failure(self, _train_engine_failure: bool):
        self._train_engine_failure = _train_engine_failure

    def get_engine_failure(self) -> bool:
        return self._train_engine_failure

    #Brake Failure
    def set_brake_failure(self, _brake_failure: bool):
        self._brake_failure = _brake_failure

    def get_brake_failure(self) -> bool:
        return self._brake_failure

    def set_heater_failure(self, _heater_failure: bool):
        self._heater_failure = _heater_failure

    def get_heater_failure(self) -> bool:
        return self._heater_failure

    def launch_ui(self):
        print("Launching Track Model UI")

        try:
            from track_model.Track_Model_UI import Ui_MainWindow
            self._ui = Ui_MainWindow(self)

        except:
            print("An error occured:")
            traceback.print_exc()
            print("Track model not initialized yet")








