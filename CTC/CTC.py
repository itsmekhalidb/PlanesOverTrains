# -- Imports -- #
import traceback
import os
import threading
import time
from typing import Callable
from datetime import datetime, timedelta

from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.ctc_track_model_api import CTCTrackModelAPI


_stations = {} # dictionary of stations and blocks


class CTC(object):
    def __init__(self, TrackCTRLSignal : CTCTrackControllerAPI, TrackModelSignal : CTCTrackModelAPI):
        # -- CTC Variables -- #
        self._trains = [] # list of train objects
        self._occupied_blocks = [] # list of occupied blocks
        self._closed_blocks = [] # list of closed blocks
        self._total_passengers = 0 # passenger count
        self._time = datetime.combine(datetime.now().date(), datetime.min.time()) # time object set to midnight
        self._elapsed_time = 0 # time object set to midnight
        self._elapsed_time = 0.0 # time in hours since time started
        self._time_scaling = 1 # how fast time is moving
        self._tick_counter = 0 # number of ticks since last second
        self._ticket_sales = 0 # number of tickets sold

        self.TrackCTRLSignal = TrackCTRLSignal
        self.TrackModelSignal = TrackModelSignal

        # run update function
        self.update()

    # getter functions
    def get_throughput(self):
        if self._elapsed_time > 0:
            return round(self._total_passengers/self._elapsed_time, 0)
        else:
            return 0
    def get_trains(self):
        return self._trains
    def get_stations_names(self):
        return _stations.keys()
    def get_time(self):
        return self._time
    def get_time_scaling(self):
        return self._time_scaling
    def get_highest_train_num(self):
        max = 1
        if not self._trains:
            return max
        else:
            for train in self._trains:
                if int(train.get_train_number()) > max:
                    max = int(train.get_train_number())
        return max + 1
    
    # setter functions
    def set_time_scaling(self, num):
        self._time_scaling = num
    def change_block(self, block):
        if block in self._closed_blocks:
            self._closed_blocks.remove(block)
        else:
            self._closed_blocks.append(block)
    
    # automatic train schedule function
    def import_schedule(self, doc):
        return 

    # manual train schedule functions
    def create_schedule(self, station_name, time_in, function, train_index):
        global _stations
        if function == 0: # new train
            # temp_trn = Train()
            # destination_block = _stations[station_name]
            # departure_time = 1
            # temp_trn.create_schedule(destination_block, station_name, time_in, departure_time)
            # self._trains.append(temp_trn)

            # code to test stuff until i get station info from api; dispatching to glenbury

            temp_trn = Train(True, str(self.get_highest_train_num()))
            destination_block = 65
            travel_time = timedelta(hours=400/70000)
            arrival_datetime = datetime.combine(datetime.now().date(), time_in)
            departure_time = arrival_datetime - travel_time
            temp_trn.create_schedule(destination_block, station_name, time_in, departure_time, self.TrackCTRLSignal)
            self._trains.append(temp_trn)
        elif function == 1: # edit existing schedule
            return
        elif function == 2: # add a stop
            return
    
    # track controller interface functions
    def get_route_info(self, train_num):
        return self._trains[train_num].get_route_info()
    def get_block_status(self, block_num):
        return self._track.get_block_status(block_num)
    def get_occupancy(self):
        return self.TrackCTRLSignal._occupancy
    def update_curr_speed(self, train_num):
        # speed = self.TrackCTRLSignal._curr_speed[train_num]
        # if speed < 1 or speed == None:
        #     speed = 0
        return 0
    def update_light_color(self, light_num, status):
        self._track.update_track(light_num, status)
    def update_switch_position(self, switch_index):
        self._track.switch_switch(switch_index)
    def update_occupancy(self, occupied_block):
        self._track.update_occupancy(occupied_block)
    def update_passenger_info(self, station, tickets_sold):
        self._track.update_tickets(station, tickets_sold)
    def update_section_status(self):
        self.TrackCTRLSignal._track_section_status = self._closed_blocks
    def check_track_info(self):
        a1_data = self.TrackCTRLSignal._green['A1']
        return a1_data[1] != 0 # return false if speed limit is 0

    
    # testbench/api functions
    def change_occupied(self, section, block):
        return
    def change_ticket_sales(self, train, passengers):
        return
    def change_current_velocity(self, train, vel):
        return
    def change_switch(self, switch, dir):
        return
    def change_light(self, color):
        return

    # update function every 100 ms
    def update(self, thread=True):
        # clock
        if self._tick_counter < 10 / self._time_scaling:
            self._tick_counter += 1
        else:
            self._tick_counter -= 10 / self._time_scaling
            self._time = self._time + timedelta(microseconds=100000 * self._time_scaling)
            self._elapsed_time = self._elapsed_time + (1 / 3600000 * self._time_scaling)
            self.TrackCTRLSignal._time = self._time

        self.TrackCTRLSignal._train_info = self.create_departures()

        # update functions
        self.update_section_status()

        # Enable Threading
        if thread:
            threading.Timer(0.0001, self.update).start()
    
    def create_departures(self):
        output = {}
        for train in self._trains:
            #if self._time >= train.get_departure_time():
                output[train.get_train_number()] = train.get_route_info()
        return output


    # launch ui from launcher
    def launch_ui(self):
        print("Launching CTC UI")
        try:
            from CTC.CTC_UI import CTC_Main_UI
            self._ui = CTC_Main_UI(self)
        except Exception as ex:
            print("An error occurred:")
            traceback.print_exc()
            print("CTC not initialized")



class Train(object):
    def __init__(self, func : Callable, train_num = -1):
        self._number = train_num # train id number
        self._actual_velocity = 0 # actual velocity of train from train controller
        self._current_block = 0 # current position of train, 0 indicates yard
        self._schedule = None # object containing train's schedule
    
    # hardcoded blue line function
    def test_blue_line_train(self, num):
        self._number = num
        
    # create schedule
    def create_schedule(self, destination_block, dest_station, arrival_time, departure_time, api):
        sched = Schedule(destination_block, dest_station, arrival_time, departure_time, api)
        self._schedule = sched
        
    # getter functions
    def get_train_number(self):
        return self._number
    def get_route_info(self):
        return self._schedule.get_route_info()
    def get_total_authority(self):
        sum = 0
        route_info = self.get_route_info()
        for key in route_info:
            block = route_info[key]
            sum = sum + block[0]
        return sum
    def get_actual_velocity(self):
        return self._actual_velocity
    def get_departure_time(self):
        return self._schedule.get_departure_time()
    def get_arrival_time(self):
        return self._schedule.get_arrival_time()
    def get_suggested_velocity(self):
        return self._schedule.get_suggested_velocity()
    def get_dest_station(self):
        return self._schedule.get_destination_station()



class Schedule(object):
    def __init__(self, dest_block, dest_station, arrival_time, departure_time, api):
        self._arrival_time = arrival_time # train arrival time from dispatcher
        self._destination_block = dest_block # train destination from dispatcher
        self._dest_station = dest_station # name of destination station
        self._departure_time = departure_time # calculated train departure time

        self._route_info = {"K63" : [100, 70],
                                 "K64" : [100, 70],
                                 "K65" : [200, 70]
                                 } # dictionary of blocks, authority in each block, and velocity for each

    # recursive function to schedule each block TO BE IMPLEMENTED


    # getter functions
    def get_suggested_velocity(self):
        return self._suggested_velocity
    def get_departure_time(self):
        return self._departure_time
    def get_arrival_time(self):
        return self._arrival_time
    def get_destination_station(self):
        return self._dest_station
    def get_route_info(self):
        return self._route_info