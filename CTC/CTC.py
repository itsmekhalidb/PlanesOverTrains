# -- Imports -- #
import traceback
import os
import threading
from datetime import datetime, timedelta

from api.ctc_track_controller_api import CTCTrackControllerAPI


_stations = {} # dictionary of stations and block ids


class CTC(object):
    def __init__(self, TrackCTRLSignal : CTCTrackControllerAPI):
        # -- CTC Variables -- #
        self._track = None # object for the track
        self._trains = [] # list of train objects

        self.TrackCTRLSignal = TrackCTRLSignal

        # run update function
        self.update()

    # hardcoded blue line function
    def test_blue_line_CTC(self):
        global _stations
        track = Track()
        track.test_blue_line_track()
        self._track = track

        for x in range(10):
            train = Train()
            train.test_blue_line_train(x+1)
            self._trains.append(train)
        
        _stations = {
            "B" : 10,
            "C" : 15
        }

    # getter functions
    def get_trains(self):
        return self._trains
    def get_stations_names(self):
        return _stations.keys()
    
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

    def update(self, thread=False):

        # Enable Threading
        if thread:
            threading.Timer(0.1, self.update).start()

    def launch_ui(self):
        print("Launching CTC UI")
        try:
            from CTC.CTC_UI import CTC_Main_UI
            self._ui = CTC_Main_UI(self)
        except Exception as ex:
            print("An error occurred:")
            traceback.print_exc()
            print("CTC not initialized")



class Track(object):
    def __init__(self):
        self._lines = [] # list of lines in the track
        self._switches = [] # list of switches in the track
        self._yard = None # object for the yard

    # hardcoded blue line function
    def test_blue_line_track(self):
        blue = Line()
        blue.test_blue_line_line()
        self._lines.append(blue)

        sw = Switch()
        sw.test_blue_line_sw()
        self._switches.append(sw)

        yard = Yard()
        yard.test_blue_line_yard()
        self._yard = yard

    # getter functions
    def get_lines(self):
        return self._lines


class Line(object):
    def __init__(self):
        self._name = "" # color of the line
        self._sections = [] # list of sections in the line

    # hardcoded blue line function
    def test_blue_line_line(self):
        self._name = "Blue"

        A = Section()
        B = Section()
        C = Section()
        A.test_blue_line_sect('A')
        B.test_blue_line_sect('B')
        C.test_blue_line_sect('C')
        self._sections.append(A)
        self._sections.append(B)
        self._sections.append(C)
    
    # getter functions
    def get_sections(self):
        return self._sections


class Section(object):
    def __init__(self):
        self._name = '' # name (letter) of the section
        self._blocks = [] # list of blocks in the section

    # hardcoded blue line function
    def test_blue_line_sect(self, name):
        self._name = name

        if name == 'A':
            for x in range(4):
                blk = Block()
                blk.test_blue_line_blk(x+1)
                self._blocks.append(blk)
        elif name == 'B':
            for x in range(4):
                blk = Block()
                blk.test_blue_line_blk(x+6)
                self._blocks.append(blk)
        else:
            for x in range(4):
                blk = Block()
                blk.test_blue_line_blk(x+11)
                self._blocks.append(blk)
    
    # getter functions
    def get_blocks(self):
        return self._blocks



class Block(object):
    def __init__(self):
        self._number = -1 # block number inside line from plc file
        self._block_id = -1 # block id for internal use
        self._length = -1 # length of block in m
        self._speed_limit = -1 # speed limit inside block in km/hr
        self._station = None # station inside block if applicable
        self._occupied = 0 # indicates what train is occupying a block, 0 if unoccupied
        self._input_blocks = [] # indicates what blocks can input to this block, 0 indicates yard
        self._output_blocks = [] # indicates what blocks this block can output to, 0 indicates yard

    # hardcoded blue line function
    def test_blue_line_blk(self, num):
        self._number = num
        self._length = 50
        self._speed_limit = 50
        if num == 10:
            B = Station()
            B.test_blue_line_stat("B")
            self._station = B
        elif num == 15:
            C = Station()
            C.test_blue_line_stat("C")
            self._station = C
        self._occupied = 0
        if (num != 1 or num != 10 or num != 11 or num != 15):
            self._input_blocks.append(num-1)
            self._input_blocks.append(num+1)
            self._output_blocks.append(num-1)
            self._output_blocks.append(num+1)
        elif (num == 1):
            self._input_blocks.append(0)
            self._output_blocks.append(0)
            self._input_blocks.append(num+1)
            self._output_blocks.append(num+1)
        elif (num == 10 or num == 15):
            self._input_blocks.append(num-1)
            self._output_blocks.append(num-1)
        elif (num == 11): # do not add 5 because the switch is pointing to 6 to start
            self._input_blocks.append(num+1)
            self._output_blocks.append(num+1)

    # return ideal traversal time in seconds
    def get_ideal_traversal_time(self):
        ms_vel = self._speed_limit * 1000 / 360
        res = self._length / ms_vel
        return res
    
    # getter function 
    def get_length(self):
        return self._length



class Station(object):
    def __init__(self):
        self._name = "" # name of station
        self._side = 2 # side of the track the station is on, 0 is left, 1 is right, 2 is both
    
    # hardcoded blue line function
    def test_blue_line_stat(self, name):
        self._name = name


class Switch(object):
    def __init__(self):
        self._position = 0 # current position of the switch, corresponds with index of block_connections
        self._input_block = -1 # block feeding into the switch after which it forks
        self._block_connections = [] # output blocks
    
    # hardcoded blue line function
    def test_blue_line_sw(self):
        self._position = 0
        self._input_block = 5
        self._block_connections.append(6)
        self._block_connections.append(11)


class Yard(object):
    def __init__(self):
        self._input_blocks = [] # blocks feeding into the yard
        self._output_blocks = [] # blocks where trains can leave the yard

    # hardcoded blue line function
    def test_blue_line_yard(self):
        self._input_blocks.append(1)
        self._output_blocks.append(1)


class Train(object):
    def __init__(self):
        self._number = -1 # train id number
        self._authority = -1 # distance train is allowed to move in meters
        self._actual_velocity = 0 # actual velocity of train from train controller
        self._current_block = 0 # current position of train, 0 indicates yard
        self._schedule = None # object containing train's schedule
    
    # hardcoded blue line function
    def test_blue_line_train(self, num):
        self._number = num

    # return train list info
    def train_list_info(self):
        if self._current_block == 0:
            return "Train " + str(self._number) + " - Idle"
        else:
            return "Train " + str(self._number) + " - Outbound"
        
    # create schedule
    def create_schedule(self, dest_station, arrival_time, track):
        global _stations
        destination_block = _stations[dest_station]
        sched = Schedule(destination_block, dest_station, arrival_time)
        self._schedule = sched
        self._authority = sched.test_blue_sched(track)
        
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
    def __init__(self, dest_block, dest_station, arrival_time):
        self._arrival_time = arrival_time # train arrival time from dispatcher
        self._destination_block = dest_block # train destination from dispatcher
        self._dest_station = dest_station # name of destination station
        self._departure_time = None # calculated train departure time
        self._suggested_velocity = 0 # calculated velocity

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