# -- Imports -- #
import traceback
import os
import threading
import time
from typing import Callable
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog
import pandas as pd

from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.ctc_track_model_api import CTCTrackModelAPI


class CTC(object):
    def __init__(self, TrackCTRLSignal : CTCTrackControllerAPI, TrackModelSignal : CTCTrackModelAPI):
        # -- CTC Variables -- #
        self._trains = [] # list of train objects
        self._stations = {} # dict of stations and their blocks
        self._occupied_blocks = [] # list of occupied blocks
        self._closed_blocks = {"green" : [], "red" : []} # list of closed blocks
        self._commanded_switches = {"green" : {}, "red" : {}} # list of commanded switch positions
        self._total_passengers = 0 # passenger count
        self._prev_passengers = 0 # passenger count
        self._seven_hours = timedelta(hours=7)
        self._time = datetime.combine(datetime.now().date(), datetime.min.time()) # time object set to midnight
        self._time = self._time + self._seven_hours
        self._prev_time = self._time
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
        if self._elapsed_time >= 3600:
            self._prev_passengers = self._total_passengers
            self._elapsed_time = 0
        return round(self._total_passengers - self._prev_passengers, 0)

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
        # our code is so dumb and for some reason using a constant of 5 makes it 10x speed
        if num == 10:
            self._time_scaling = 5
        else:
            self._time_scaling = num
    def change_block(self, line, block):
        if block in self._closed_blocks[line]:
            self._closed_blocks[line].remove(block)
            self.TrackCTRLSignal._track_section_status[block] = 0
        elif block not in self._closed_blocks[line]:
            self._closed_blocks[line].append(block)
            self.TrackCTRLSignal._track_section_status[block] = 1
    
    # automatic train schedule function
    def import_schedule(self, doc, line):
        tim = self._time
        for index, row in doc.iloc[1:].iterrows():
            station = ""
            t = timedelta(0)
            for column, value in row.items():
                if column == "Line" and value.lower() != line:
                    break
                elif column == "Infrastructure":
                    name = value[9:]
                    station = self.to_camel_case(name)
                elif column == "total time to station w/dwell (min)":
                    t = timedelta(minutes=int(value))
                    # print(t)
            if station in self._stations[line].keys():
                res1 = self.create_schedule(station, tim+t, 0, -1, line)
                if res1 == 1:
                    tim += t
                else:
                    res2 = self.create_schedule(station, tim+res1+t, 0, -1, line)
                    if res2 == 1:
                        tim = tim + t + res1
                    else:
                        print("idk time bad no work!")



    # manual train schedule functions
    def create_schedule(self, station_name, time_in, function, train_index, line):
        try:
            if function == 0: # new train
                temp_trn = Train(True, self.get_highest_train_num())
                destination_block = min(self._stations[line][station_name])
                arrival_datetime = datetime.combine(datetime.now().date(), time_in.time())
                time_to_arrival = arrival_datetime - self.get_time()
                x = temp_trn.create_schedule(destination_block, 0, station_name, arrival_datetime, time_to_arrival, line, self.TrackCTRLSignal)
                if temp_trn.sched_exists() == 1:
                    self._trains.append(temp_trn)
                    return 1
                else:
                    return x
                return 0
            elif function == 1: # delete existing schedule
                return
            elif function == 2: # add a stop
                train = self._trains[train_index]
                destination_block = min(self._stations[line][station_name])
                arrival_datetime = datetime.combine(datetime.now().date(), time_in.time())
                time_to_arrival = arrival_datetime - self.get_time()
                train.create_schedule(destination_block, 0, station_name, arrival_datetime, time_to_arrival, line, self.TrackCTRLSignal)
        except Exception as e:
            traceback.print_exc()
            print(e)
            return
    
    # track controller interface functions
    def get_sections(self, line):
        return self.TrackCTRLSignal._track_info.get_section_list(line)
    def get_switches(self, line):
        return self.TrackCTRLSignal._switch[line]
    def get_switch_pos(self, line, num):
        return self.TrackCTRLSignal._switch[line.capitalize()][num]
    def get_blocks(self, line, section):
        return self.TrackCTRLSignal._track_info.get_block_list(line, section)
    def get_stations(self):
        try:
            self._stations = self.TrackCTRLSignal._track_info.get_station_list()
            return self._stations
        except Exception as e:
            print(e)
            return {}
    def get_occupancy(self, line):
        output = list(self.TrackCTRLSignal._occupancy.values()).extend(list(self._closed_blocks[line]))
        if output == None:
            output = []
        return output
    def get_curr_speed(self, train_num):
        speed = self._trains[train_num-1].get_actual_velocity()
        if speed < 1 or speed == None:
            speed = 0
        return speed
    def update_switch(self, line, switch, pos):
        self._commanded_switches[line][switch] = pos
    def clear_maintenance(self, line):
        self._closed_blocks[line] = []
        self._commanded_switches[line] = {}
    def update_authorities(self):
        for train in self._trains:
            train.update_authority(self._time_scaling)
    def check_filepath(self):
        return self.TrackCTRLSignal._filepath != ""

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
                if self._time.second != self._prev_time.second:
                    # self._elapsed_time += self._elapsed_time + (1 / 3600000 * self._time_scaling)
                    self._elapsed_time += 1
                self._prev_time = self._time
                self.TrackCTRLSignal._time = self._time

            self.TrackCTRLSignal._train_out = self.create_departures()
            for train in self._trains:
                self.TrackCTRLSignal._train_ids.add(train.get_train_number())

            # print(self.TrackModelSignal._ticket_sales)
            # update functions
            # self.update_section_status()
            # print(self.TrackCTRLSignal._train_out)
            self.read_train_in()

            # update ticket sales
            for train in self.TrackModelSignal._ticket_sales:
                if len(train) > 1:
                    self._total_passengers = train[1]


        # Enable Threading
        if thread:
            threading.Timer(0.01, self.update).start()


    def create_departures(self):
        try:
            output = {}
            for train in self._trains:
                if self._time >= train.get_departure_time():
                    num = train.get_train_number()
                    output[num] = train.get_curr_auth_speed_info()
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
            self._trains[i].set_actual_velocity(train[0])
            self._trains[i].set_current_block(train[1])
            self._trains[i].set_cum_distance(train[2])
            i = i+1


    # type conversion functions
    def to_camel_case(self, variable_name):
        parts = variable_name.split(' ')
        camel_case = ' '.join(word.capitalize() for word in parts)
        return camel_case

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
        self._commanded_velocity = -1 # commanded velocity from ui, -1 means don't use
        self._current_block = 0 # current position of train, 0 indicates yard
        self._schedule = [] # object containing train's schedule
    
    # hardcoded blue line function
    def test_blue_line_train(self, num):
        self._number = num
        
    # create schedule
    def create_schedule(self, destination_block, starting_block, dest_station, arrival_time, time_to_arrival, line, api):
        # print(len(self._schedule))
        if len(self._schedule) < 1: # first schedule
            sched = Schedule(starting_block, destination_block, dest_station, arrival_time, 1, -1, line, api)
            if sched._total_time < time_to_arrival:
                self._schedule.append(sched)
                if self._schedule[-1]._last_block == 0:
                    self._schedule.pop()
                self.yard_schedule(destination_block, sched.get_last_dir(), sched.get_arrival_time(), line, api)
            else:
                print("fuck you fucking idiot thats too fucking early it takes", sched._total_time, "to get there")
                return sched._total_time
        else: # adding stops
            self._schedule.pop() # remove schedule going back to yard
            sched = Schedule(int(self._schedule[-1]._last_block), int(destination_block), dest_station, arrival_time, 1, self._schedule[-1]._last_dir, line, api)
            tiem = timedelta(0)
            for s in self._schedule:
                tiem += s._total_time
            tiem += sched._total_time
            if tiem < time_to_arrival:
                self._schedule.append(sched)
                self.yard_schedule(destination_block, sched.get_last_dir(), sched.get_arrival_time(), line, api)
            else:
                print("fuck you fucking idiot thats too fucking early it takes", tiem, "to get there")
                return tiem
        
        # for s in self._schedule:
        #     print(s._route_info)

    # create schedule going back to yard
    def yard_schedule(self, starting_block, last_dir, arr_time, line, api):
        sched = Schedule(starting_block, 0, "Yard", arr_time, 0, last_dir, line, api)
        self._schedule.append(sched)

    # update authority
    def update_authority(self, time_scaling):
        # move to next schedule if this one's done
        # if self.get_total_authority() <= 0:
        #     self._schedule.pop(0)
        self._schedule[0].update_authority(self._actual_velocity, self._current_block, time_scaling)
        
    # getter functions
    def get_train_number(self):
        return self._number
    def get_route_info(self):
        return self._schedule[0].get_route_info()
    def get_curr_authority(self):
        return self._schedule[0]._curr_authority
    def get_total_authority(self):
        return self._schedule[0]._total_authority
    def sched_exists(self):
        return len(self._schedule) != 0
    def get_actual_velocity(self):
        return self._actual_velocity
    def get_departure_time(self):
        return self._schedule[0].get_departure_time()
    def get_arrival_time(self):
        return self._schedule[0].get_arrival_time()
    def get_commanded_speed(self):
        return self._commanded_velocity
    def get_suggested_velocity(self):
        return self._schedule[0].get_curr_sugg_speed(self._current_block)
    def get_dest_station(self):
        return self._schedule[0].get_destination_station()
    def get_curr_auth_speed_info(self):
        if self.get_commanded_speed() != -1:
            return [self.get_curr_authority(), min(self._schedule[0].get_curr_sugg_speed(self._current_block), self.get_commanded_speed())]
        else:
            return [self.get_curr_authority(), self._schedule[0].get_curr_sugg_speed(self._current_block)]
    
    # setter functions
    def set_actual_velocity(self, vel):
        self._actual_velocity = vel
    def set_current_block(self, blk):
        self._current_block = blk
    def set_cum_distance(self, cd):
        self._schedule[0].update_cum_distance(cd, self._current_block)



class Schedule(object):
    # i_block is starting point
    # o_block is destination
    # tim is arrival time for outbound, departure time for inbound
    def __init__(self, i_block, o_block, dest_station, tim, outbound, last_dir, line, api: CTCTrackControllerAPI):
        self._api = api
        # make route info to station
        self._route_info = {}
        self._total_authority = 0
        self._curr_authority = 0
        self._total_time = timedelta()
        self._prev_cum_distance = 0
        self._line = line

        self._blocks_arrs = []
        self._temp_block_arr = []
        self._tracker = 0
        # self._temp_block_arr.append(0)
        self._station_info = self._api._track_info.get_station_list()[self._line]
        self._arr_num = 0

        self._switches = self._api._track_info.get_khalids_special_switch_list(self._line)
        self._switch_states = []

        if outbound == 1: # going to station
            output = self.get_blocks_to_dest(self._line, o_block, i_block, [])
            for block in output[0]:
                if block != 0:
                    info = self._api._track_info.get_block_info(self._line, block)
                    # route info stuff
                    if str(block) not in self._route_info: # first appearance of block in this route
                        if block == o_block or (block != 0 and block == i_block): # halfway through station block
                            self._route_info[str(block)] = [[info['length']/2], info['speed limit']]
                            self._total_authority = self._total_authority + info['length']/2
                            self._total_time = self._total_time + timedelta(hours=((info['length']/2000)/info['speed limit']))
                        else:
                            self._route_info[str(block)] = [[info['length']], info['speed limit']]
                            self._total_authority = self._total_authority + info['length']
                            self._total_time = self._total_time + timedelta(hours=((info['length']/1000)/info['speed limit']))
                        # calculate time
                    else: # not the first appearance
                        if block == o_block: # halfway through station block
                            self._route_info[str(block)][0].append(info['length']/2)
                            self._total_authority = self._total_authority + info['length']/2
                            self._total_time = self._total_time + timedelta(hours=((info['length']/2000)/info['speed limit']))
                        else:
                            self._route_info[str(block)][0].append(info['length'])
                            self._total_authority = self._total_authority + info['length']
                            self._total_time = self._total_time + timedelta(hours=((info['length']/1000)/info['speed limit']))
            self._arrival_time = tim # train arrival time from dispatcher
            self._departure_time = self._arrival_time - self._total_time # calculate train departure time
            self._destination_block = o_block # train destination from dispatcher
            self._dest_station = dest_station # name of destination station
            self._starting_block = 0 # start at yard
            self._yard_block = 0 # yard, where trains start
            self._last_dir = output[1] # last direction the train is facing, for going back to yard/next station

        else: # going to yard
            output = self.get_blocks_to_yard(self._line, i_block, i_block, last_dir, [])
            for block in output:
                if block != 0:
                    info = self._api._track_info.get_block_info(self._line, block)
                    if str(block) not in self._route_info: # first appearance of block in this route
                        if block == i_block: # halfway through station block
                            self._route_info[str(block)] = [[info['length']/2], info['speed limit']]
                            self._total_authority = self._total_authority + info['length']/2
                            self._total_time = self._total_time + timedelta(hours=((info['length']/2000)/info['speed limit']))
                        else:
                            self._route_info[str(block)] = [[info['length']], info['speed limit']]
                            self._total_authority = self._total_authority + info['length']
                            self._total_time = self._total_time + timedelta(hours=((info['length']/1000)/info['speed limit']))
                        # calculate time
                    else: # not the first appearance
                        if block == i_block: # halfway through station block
                            self._route_info[str(block)][0].append(info['length']/2)
                            self._total_authority = self._total_authority + info['length']/2
                            self._total_time = self._total_time + timedelta(hours=((info['length']/2000)/info['speed limit']))
                        else:
                            self._route_info[str(block)][0].append(info['length'])
                            self._total_authority = self._total_authority + info['length']
                            self._total_time = self._total_time + timedelta(hours=((info['length']/1000)/info['speed limit']))
                else:
                    self._route_info[str(block)] = [[1], 100]
                    self._total_authority = self._total_authority + 1
                    self._total_time = self._total_time + timedelta(seconds=.1)
            self._departure_time = tim # train departure time from previous schedule
            self._arrival_time = self._departure_time + self._total_time # calculate train arrival time
            self._destination_block = 0 # train destination from dispatcher
            self._dest_station = dest_station # name of destination station
            self._starting_block = i_block # start at station
            self._yard_block = 0 # yard, where trains start
            self._last_dir = -1 # who cares

        self._last_block = next(iter(self._route_info))
        print("cool arrays: ", self._blocks_arrs)
        # print(self._route_info)
        # print(self._total_time)

    # get blocks between yard and station
    def get_blocks_to_dest(self, line, dest_block, curr_block = 0, result = [], dir = 1):
        # block arr stuff
        self._temp_block_arr.append(curr_block)
        if any(curr_block in array for array in self._station_info.values()):
            self._blocks_arrs.append(self._temp_block_arr)
            self._temp_block_arr = []
            self._temp_block_arr.append(curr_block)

        if curr_block == dest_block: # at station
            result.append([])
            result.append(dir)
            result[0].append(curr_block)

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
                if line == "green": # only multiple options for the one going to yard, don't go to yard
                    for entry in options:
                        if entry != "name" and entry != "0":
                            next_block = int(entry)
                            dir = options[entry][0]
                            break
                elif line == "red":
                    print("meow")

            result = self.get_blocks_to_dest(line, dest_block, next_block, result, dir)
            result[0].append(curr_block)

        else: # next block is a block
            # determine next_block
            if dir == 1:
                next_block = curr_block+1
            else:
                next_block = curr_block-1
            result = self.get_blocks_to_dest(line, dest_block, next_block, result, dir)
            result[0].append(curr_block)
        
        return result

    # return to yard
    def get_blocks_to_yard(self, line, curr_block, starting_block, dir, result = []):
        # block arr stuff
        self._temp_block_arr.append(curr_block)
        if any(curr_block in array for array in self._station_info.values()):
            self._blocks_arrs.append(self._temp_block_arr)
            self._temp_block_arr = []
            self._temp_block_arr.append(curr_block)
        dest_block = 0
        if curr_block == dest_block: # at yard
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
                if line == "green": # only multiple options for the one going to yard, go to yard
                    for entry in options:
                        if entry == "0":
                            next_block = int(entry)
                            dir = options[entry][0]
                            break
                elif line == "red":
                    print("meow")

            result = self.get_blocks_to_yard(line, next_block, starting_block, dir, result)
            result.append(curr_block)

        else: # next block is a block
            # determine next_block
            if dir == 1:
                next_block = curr_block+1
            else:
                next_block = curr_block-1
            result = self.get_blocks_to_yard(line, next_block, starting_block, dir, result)
            result.append(curr_block)
        return result

    # getter functions
    def get_last_dir(self):
        return self._last_dir
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
    def get_curr_authority(self):
        return self._curr_authority
    def get_curr_sugg_speed(self, curr_block):
        if str(curr_block) in self._route_info:
            return self._route_info[str(curr_block)][1]
        else:
            return 0

    def update_cum_distance(self, cd, curr_block):
        if str(curr_block) in self._route_info:
            # find the index of the first nonzero value in the array
            nonzero_index = next((i for i, value in enumerate(self._route_info[str(curr_block)][0]) if value != 0), len(self._route_info[str(curr_block)][0]) - 1)

            cum_change = cd - self._prev_cum_distance
            self._prev_cum_distance = cd

            if cum_change < 0: # moved on to next block
                self._tracker = 0
                # find the index of the first nonzero value in the previous block
                nonzero_index_prev = next((i for i, value in enumerate(self._route_info[str(curr_block-1)][0]) if value != 0), len(self._route_info[str(curr_block-1)][0]) - 1)
                cum_change = 0
                self._route_info[str(curr_block)][0][nonzero_index] += self._route_info[str(curr_block-1)][0][nonzero_index_prev]
                self._route_info[str(curr_block-1)][0][nonzero_index_prev] = 0
            # if cum_change != 0:
            #     print(cd, self._api._track_info.get_block_info(self._line, curr_block)['length']/2)
            if any(curr_block in array for array in self._station_info.values()) and cd >= self._api._track_info.get_block_info(self._line, curr_block)['length']/2 and self._tracker == 0: # if it's a station block and we're past halfway
                self._tracker = 1
                self._arr_num += 1
                # print(self._blocks_arrs[self._arr_num])

            self._route_info[str(curr_block)][0][nonzero_index] -= cum_change
            
            # print(self._route_info)

            self.update_authority(curr_block, nonzero_index)

    def update_authority(self, curr_block, nonzero_index):
        res1 = 0
        res2 = 0
        # total authority 
        for block in self._route_info:
            res1 = res1 + sum(self._route_info[block][0])
        self._total_authority = res1

        # add authorities in this array
        if self._arr_num < len(self._blocks_arrs):
            curr_arr = self._blocks_arrs[self._arr_num]
            for block in curr_arr:
                block_pos = curr_arr.index(block)
                curr_block_pos = curr_arr.index(curr_block)
                if block_pos == curr_block_pos: # block train is on in this stretch between stations
                    res2 += self._route_info[str(curr_block)][0][nonzero_index]
                    if any(block in array for array in self._station_info.values()): # if it's a station block
                        info = self._api._track_info.get_block_info(self._line, block)
                        res2 -= info['length']/2
                elif block_pos > curr_block_pos: # blocks after the one train is on
                    new_nonzero = next((i for i, value in enumerate(self._route_info[str(block)][0]) if value != 0), len(self._route_info[str(block)][0]) - 1)
                    if any(block in array for array in self._station_info.values()): # if it's a station block
                        res2 += self._route_info[str(block)][0][new_nonzero]/2
                    else:
                        res2 += self._route_info[str(block)][0][new_nonzero]
        
        # stop for red light
        if str(curr_block+1) in self._api._light and self._api._light[str(curr_block+1)] == 1:
            res2 = 0
        self._curr_authority = res2