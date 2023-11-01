# -- Imports -- #
import traceback
import os
import threading
import time
from typing import Callable
from datetime import datetime, timedelta

from api.ctc_track_controller_api import CTCTrackControllerAPI


_stations = {} # dictionary of stations and blocks


class CTC(object):
    def __init__(self, TrackCTRLSignal : CTCTrackControllerAPI):
        # -- CTC Variables -- #
        self._trains = [] # list of train objects
        self._occupied_blocks = [] # list of occupied blocks
        self._closed_blocks = [] # list of closed blocks
        self._total_passengers = 0 # passenger count
        self._time = datetime.combine(datetime.now().date(), datetime.min.time()) # time object set to midnight
        self._time_scaling = 1 # how fast time is moving
        self._tick_counter = 0 # number of ticks since last second

        self.TrackCTRLSignal = TrackCTRLSignal

        # run update function
        self.update()

    # getter functions
    def get_trains(self):
        return self._trains
    def get_stations_names(self):
        return _stations.keys()
    def get_time(self):
        return self._time
    
    # setter functions
    def set_time_scaling(self, num):
        self._time_scaling = num
    
    #automatic train schedule function
    def import_schedule(self, doc):
        return

    # manual train schedule functions
    def create_schedule(self, station_name, time_in, function, train_index):
        global _stations
        if function == 0: # new train
            temptrn = Train()
            destination_block = _stations[station_name]
            departure_time = 1
            suggested_velocity = 1
            temptrn.create_schedule(destination_block, station_name, time_in, departure_time, suggested_velocity)
            self._trains.append(temptrn)
        elif function == 1: # edit existing schedule
            return
        elif function == 2: # add a stop
            return
    
    def close_block(self, section, block):
        return
    
    def calculate_throughput(self):
        return
    
    # track controller interface functions
    def get_authority(self, train_num):
        return self._trains[train_num].get_authority()
    def get_suggested_speed(self, train_num):
        return self._trains[train_num].get_suggested_velocity()
    def get_block_status(self, block_num):
        return self._track.get_block_status(block_num)
    def update_light_color(self, light_num, status):
        self._track.update_track(light_num, status)
    def update_switch_position(self, switch_index):
        self._track.switch_switch(switch_index)
    def update_occupancy(self, occupied_block):
        self._track.update_occupancy(occupied_block)
    def update_passenger_info(self, station, tickets_sold):
        self._track.update_tickets(station, tickets_sold)
    
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
        if (self._tick_counter < 10/self._time_scaling):
            self._tick_counter += 1
        else:
            self._tick_counter = 0
            self._time = self._time + timedelta(seconds=1)
            self.TrackCTRLSignal._time = self._time

        # Enable Threading
        if thread:
            threading.Timer(0.1, self.update).start()

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
    def __init__(self, func : Callable):
        self._number = -1 # train id number
        self._actual_velocity = 0 # actual velocity of train from train controller
        self._current_block = 0 # current position of train, 0 indicates yard
        self._schedule = None # object containing train's schedule
    
    # hardcoded blue line function
    def test_blue_line_train(self, num):
        self._number = num
        
    # create schedule
    def create_schedule(self, destination_block, dest_station, arrival_time, departure_time, suggested_velocity):
        sched = Schedule(destination_block, dest_station, arrival_time, departure_time, suggested_velocity)
        self._schedule = sched
        
    # getter functions
    def get_authority(self):
        return self._authority
    def get_actual_velocity(self):
        return self._actual_velocity
    def get_departure_time(self):
        return self._schedule.get_departure_time()
    def get_arrival_time(self):
        return self._schedule.get_arrival_time()
    def get_suggested_velocity(self):
        return self._schedule.get_suggested_velocity()



class Schedule(object):
    def __init__(self, dest_block, dest_station, arrival_time, departure_time, suggested_velocity):
        self._arrival_time = arrival_time # train arrival time from dispatcher
        self._destination_block = dest_block # train destination from dispatcher
        self._dest_station = dest_station # name of destination station
        self._departure_time = departure_time # calculated train departure time
        self._suggested_velocity = suggested_velocity # calculated velocity
        self._route_authority = {} # dictionary of blocks and the authority in each block

    # recursive function to schedule each block TO BE IMPLEMENTED

    # temporary blue line scheduling function
    def test_blue_sched(self, track):
        lines = track.get_lines()
        sections = lines[0].get_sections()
        total_time = 0 # total travel time in seconds
        total_dist = 0 # total distance in meters
        # calculate travel time
        if self._destination_block == 10:
            for x in sections[0].get_blocks():
                total_time += x.get_ideal_traversal_time()
                total_dist += x.get_length()
            for x in sections[1].get_blocks():
                total_time += x.get_ideal_traversal_time()
                total_dist += x.get_length()
        elif self._destination_block == 15:
            for x in sections[0].get_blocks():
                total_time += x.get_ideal_traversal_time()
                total_dist += x.get_length()
            for x in sections[2].get_blocks():
                total_time += x.get_ideal_traversal_time()
                total_dist += x.get_length()
        arrival_time_with_date = datetime.combine(datetime.today(), self._arrival_time)
        temp_departure_time = arrival_time_with_date - timedelta(minutes=total_time) # I CHANGED THIS TO MINUTES SO IT'S NOT INSTANTANEOUS
        self._departure_time = temp_departure_time.time()
        self._suggested_velocity = 50
        return total_dist
            

    # getter functions
    def get_suggested_velocity(self):
        return self._suggested_velocity
    def get_departure_time(self):
        return self._departure_time
    def get_arrival_time(self):
        return self._arrival_time
    def get_destination_station(self):
        return self._dest_station