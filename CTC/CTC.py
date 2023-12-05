# -- Imports -- #
import traceback
import os
import threading
import time
from typing import Callable
from datetime import datetime, timedelta

from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.ctc_track_model_api import CTCTrackModelAPI


class CTC(object):
    def __init__(self, TrackCTRLSignal : CTCTrackControllerAPI, TrackModelSignal : CTCTrackModelAPI):
        # -- CTC Variables -- #
        self._trains = [] # list of train objects
        self._stations = {} # dict of stations and their blocks
        self._occupied_blocks = [] # list of occupied blocks
        self._closed_blocks = [] # list of closed blocks
        self._total_passengers = 0 # passenger count
        self._seven_hours = timedelta(hours=7)
        self._time = datetime.combine(datetime.now().date(), datetime.min.time()) # time object set to midnight
        self._time = self._time + self._seven_hours
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
    def get_stations_names(self, line):
        return self._stations[line]
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
    def index_from_num(self, num):
        i = 0
        for train in self._trains:
            if train.get_train_number() == num:
                return i
            i = i+1
        return -1
    
    # setter functions
    def set_time_scaling(self, num):
        self._time_scaling = num
    def change_block(self, block):
        if block in self._closed_blocks:
            self._closed_blocks.remove(block)
            self.TrackCTRLSignal._track_section_status[block] = 0
        elif block not in self._closed_blocks:
            self._closed_blocks.append(block)
            self.TrackCTRLSignal._track_section_status[block] = 1
    
    # automatic train schedule function
    def import_schedule(self, doc):
        return 

    # manual train schedule functions
    def create_schedule(self, station_name, time_in, function, train_index):
        try:
            if function == 0: # new train
                temp_trn = Train(True, self.get_highest_train_num())
                destination_block = min(self._stations['green'][station_name])
                arrival_datetime = datetime.combine(datetime.now().date(), time_in.time())
                time_to_arrival = arrival_datetime - self.get_time()
                temp_trn.create_schedule(destination_block, station_name, arrival_datetime, time_to_arrival, self.TrackCTRLSignal)
                if temp_trn.sched_exists() == 1:
                    self._trains.append(temp_trn)
            elif function == 1: # edit existing schedule
                return
            elif function == 2: # add a stop
                return
        except Exception as e:
            traceback.print_exc()
            print(e)
            return
    
    # track controller interface functions
    def get_sections(self, line):
        return self.TrackCTRLSignal._track_info.get_section_list(line)
    def get_blocks(self, line, section):
        return self.TrackCTRLSignal._track_info.get_block_list(line, section)
    def get_stations(self):
        try:
            self._stations = self.TrackCTRLSignal._track_info.get_station_list()
            return self._stations
        except Exception as e:
            print(e)
            return {}
    def get_block_status(self, block_num):
        return self._track.get_block_status(block_num)
    def get_occupancy(self):
        return list(self.TrackCTRLSignal._occupancy.values()) + list(self._closed_blocks)
    def get_curr_speed(self, train_num):
        speed = self._trains[train_num-1].get_actual_velocity()
        if speed < 1 or speed == None:
            speed = 0
        return speed
    def update_light_color(self, light_num, status):
        self._track.update_track(light_num, status)
    def update_switch_position(self, switch_index):
        self._track.switch_switch(switch_index)
    def update_occupancy(self, occupied_block):
        self._track.update_occupancy(occupied_block)
    def update_passenger_info(self, station, tickets_sold):
        self._track.update_tickets(station, tickets_sold)
    # def update_section_status(self):
    #     self.TrackCTRLSignal._track_section_status = self._closed_blocks
    def update_authorities(self):
        for train in self._trains:
            if train.get_actual_velocity() != 0:
                train.update_authority(self._time_scaling)
                # print(train.get_train_number(), train.get_total_auth_speed_info())
    def check_filepath(self):
        return self.TrackCTRLSignal._filepath != ""

    
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
        with threading.Lock():
            # clock
            if self._time_scaling == 0:
                pass
            elif self._tick_counter < 10 / self._time_scaling:
                self._tick_counter += 1
            else:
                self._tick_counter -= 10 / self._time_scaling
                self._time = self._time + timedelta(microseconds=100000 * self._time_scaling)
                self._elapsed_time = self._elapsed_time + (1 / 3600000 * self._time_scaling)
                self.TrackCTRLSignal._time = self._time
                self.update_authorities()

            self.TrackCTRLSignal._train_out = self.create_departures()
            for train in self._trains:
                self.TrackCTRLSignal._train_ids.add(train.get_train_number())

            # print(self.TrackModelSignal._ticket_sales)
            # update functions
            # self.update_section_status()
            # print(self.TrackCTRLSignal._train_out)
            self.read_train_in()


        # Enable Threading
        if thread:
            threading.Timer(0.01, self.update).start()


    def create_departures(self):
        try:
            output = {}
            for train in self._trains:
                if self._time >= train.get_departure_time():
                    num = train.get_train_number()
                    # print(num)
                    # print(self.TrackCTRLSignal._train_in)
                    output[num] = train.get_total_auth_speed_info()
                    # print("block", train._current_block)
                    # print("ctc auth, curr speed: " + str([train.get_total_authority(), train.get_actual_velocity()]))
                    # print("ctc auth, sugg speed: " + str(output[num]))
                else:
                    num = train.get_train_number()
                    output[num] = [0, 0]
            return output
        except Exception as e:
            traceback.print_exc()
            print(e)
            return {}
        

    def read_train_in(self):
        i = 0
        for train in self.TrackCTRLSignal._train_in:
            # print("act_vel: " + str(train[0]))
            self._trains[i].set_actual_velocity(train[0])
            self._trains[i].set_current_block(train[1])
            i = i+1


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
        self._actual_velocity = 0 # actual velocity of train from train controller (m/s)
        self._current_block = 63 # current position of train, 0 indicates yard
        self._schedule = None # object containing train's schedule
    
    # hardcoded blue line function
    def test_blue_line_train(self, num):
        self._number = num
        
    # create schedule
    def create_schedule(self, destination_block, dest_station, arrival_time, time_to_arrival, api):
        sched = Schedule(destination_block, dest_station, arrival_time, api)
        if sched._total_time < time_to_arrival:
            self._schedule = sched

    # update authority
    def update_authority(self, time_scaling):
        self._schedule.update_authority(self._actual_velocity, self._current_block, time_scaling)
        
    # getter functions
    def get_train_number(self):
        return self._number
    def get_route_info(self):
        return self._schedule.get_route_info()
    def get_total_authority(self):
        return self._schedule._total_authority
    def sched_exists(self):
        return self._schedule != None
    def get_actual_velocity(self):
        return self._actual_velocity
    def get_departure_time(self):
        return self._schedule.get_departure_time()
    def get_arrival_time(self):
        return self._schedule.get_arrival_time()
    def get_suggested_velocity(self):
        return self._schedule.get_curr_sugg_speed(self._current_block)
    def get_dest_station(self):
        return self._schedule.get_destination_station()
    def get_total_auth_speed_info(self):
        return [self.get_total_authority(), self._schedule.get_curr_sugg_speed(self._current_block)]
        # return [self.get_total_authority(), 70.0]
    
    # setter functions
    def set_actual_velocity(self, vel):
        self._actual_velocity = vel
    def set_current_block(self, blk):
        self._current_block = blk



class Schedule(object):
    def __init__(self, dest_block, dest_station, arrival_time, api: CTCTrackControllerAPI):
        self._api = api
        # make route info to station
        self._route_info = {}
        self._total_authority = 0
        self._total_time = timedelta()
        self._switches = self._api._track_info.get_switch_list("green")
        self._switch_states = []
        for block in self.get_blocks_from_yard("green", dest_block):
            info = self._api._track_info.get_block_info('green', block)
            if str(block) not in self._route_info: # first appearance of block in this route
                if block == dest_block: # halfway through station block
                    self._route_info[str(block)] = [[info['length']/2], info['speed limit']]
                    self._total_authority = self._total_authority + info['length']/2
                    self._total_time = self._total_time + timedelta(hours=((info['length']/2000)/info['speed limit']))
                else:
                    self._route_info[str(block)] = [[info['length']], info['speed limit']]
                    self._total_authority = self._total_authority + info['length']
                    self._total_time = self._total_time + timedelta(hours=((info['length']/1000)/info['speed limit']))
                # calculate time
            else: # not the first appearance
                if block == dest_block: # halfway through station block
                    self._route_info[str(block)][0].append(info['length']/2)
                    self._total_authority = self._total_authority + info['length']/2
                    self._total_time = self._total_time + timedelta(hours=((info['length']/2000)/info['speed limit']))
                else:
                    self._route_info[str(block)][0].append(info['length'])
                    self._total_authority = self._total_authority + info['length']
                    self._total_time = self._total_time + timedelta(hours=((info['length']/1000)/info['speed limit']))

        print(self._route_info)
        self._arrival_time = arrival_time # train arrival time from dispatcher
        self._departure_time = self._arrival_time - self._total_time # calculate train departure time
        self._destination_block = dest_block # train destination from dispatcher
        self._dest_station = dest_station # name of destination station
        self._yard_block = 63 # block where trains leave yard, hard coded for now

    # get blocks between yard and station
    def get_blocks_from_yard(self, line, dest_block, curr_block = 63, result = [], dir = 1):
        if curr_block == dest_block: # at station
            result.append(curr_block)

        elif str(curr_block) in self._switches: # this block is a switch
            options = self._switches[str(curr_block)]
            if len(options) == 2: # one option of where to go
                for entry in options:
                    if entry != "name": # the place it can go
                        if (dir == options[entry][1]):
                            next_block = int(entry)
                            dir = options[entry][0]
                            break
                        else:
                            if dir == 1:
                                next_block = curr_block+1
                            else:
                                next_block = curr_block-1
                # self._switch_states.append([options["name"], ) # for forks at red line
            else: # more than one option
                print("meow")
            result = self.get_blocks_from_yard(line, dest_block, next_block, result, dir)
            result.append(curr_block)

        else: # next block is a block
            # determine next_block
            if dir == 1:
                next_block = curr_block+1
            else:
                next_block = curr_block-1
            result = self.get_blocks_from_yard(line, dest_block, next_block, result, dir)
            result.append(curr_block)
        return result

    # return to yard
    def get_blocks_to_yard(self, line, curr_block, result = []):
        dest_block = 57
        if curr_block == dest_block: # at yard
            pass
        elif self._api._track_info.get_block_info(line, curr_block+1)['switch position'] == True: # next block is a switch
            next_block = self._api._switch[curr_block+1]
            result = self.get_blocks_to_yard(line, next_block, result)
            result.append(curr_block)
        else: # next block is a block
            next_block = curr_block+1
            result = self.get_blocks_to_yard(line, next_block, result)
            result.append(curr_block)
        return result

    # getter functions
    def get_departure_time(self):
        return self._departure_time
    def get_arrival_time(self):
        return self._arrival_time
    def get_destination_station(self):
        return self._dest_station
    def get_route_info(self):
        return self._route_info
    def get_total_authority(self):
        return self._total_authority
    def get_curr_sugg_speed(self, curr_block):
        if str(curr_block) in self._route_info:
            return self._route_info[str(curr_block)][1]
        else:
            return 0

    def update_authority(self, actual_velocity, curr_block, time_scaling):
        if str(curr_block) in self._route_info:
            meters_s = actual_velocity
            # meters_s = actual_velocity * (1000/3600)
            change = meters_s * time_scaling * 0.1
            # find the index of the first nonzero value in the array
            nonzero_index = next((i for i, value in enumerate(self._route_info[str(curr_block)][0]) if value != 0), None)

            if curr_block != self._yard_block and nonzero_index is not None:
                change = change - self._route_info[str(curr_block)][0][nonzero_index]
                self._route_info[str(curr_block)][0][nonzero_index] = 0
            # print("CTC: change: " + str(change) + " route_info:" + str(self._route_info[str(curr_block)][0]) + " meters_s: " + str(meters_s))
            self._route_info[str(curr_block)][0][nonzero_index] = self._route_info[str(curr_block)][0][nonzero_index] - change
            print(self._route_info)
            self.update_total_authority()

    def update_total_authority(self):
        res = 0
        for block in self._route_info:
            res = res + sum(self._route_info[block][0])
        self._total_authority = res
