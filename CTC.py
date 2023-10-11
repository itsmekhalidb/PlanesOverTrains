# -- Imports -- #
import os
import threading


class CTC(object):
    def __init__(self):
        # -- CTC Variables -- #
        self._track = None # object for the track
        self._trains = [] # list of train objects

        # run update function
        self.update()

    # hardcoded blue line function
    def test_blue_plc_CTC(self):
        track = Track()
        track.test_blue_plc_track()
        self._track = track

        for x in range(10):
            train = Train()
            train.test_blue_plc_train(x+1)

    def update(self, thread=False):

        # Enable Threading
        if thread:
            threading.Timer(0.1, self.update).start()



class Track(object):
    def __init__(self):
        self._lines = [] # list of lines in the track
        self._switches = [] # list of switches in the track
        self._yard # object for the yard

    # hardcoded blue line function
    def test_blue_plc_track(self):
        blue = Line()
        blue.test_blue_plc_line()
        self._lines.append(blue)

        sw = Switch()
        sw.test_blue_plc_sw()
        self._switches.append(sw)

        yard = Yard()
        yard.test_blue_plc_yard()
        self._yard = yard


class Line(object):
    def __init__(self):
        self._name = "" # color of the line
        self._sections = [] # list of sections in the line
        self._stations = [] # list of sections that have a station 

    # hardcoded blue line function
    def test_blue_plc_line(self):
        self._name = "Blue"

        A = Section()
        B = Section()
        C = Section()
        A.test_blue_plc_sect('A')
        B.test_blue_plc_sect('B')
        C.test_blue_plc_sect('C')


class Section(object):
    def __init__(self):
        self._name = '' # name (letter) of the section
        self._blocks = [] # list of blocks in the section

    # hardcoded blue line function
    def test_blue_plc_sect(self, name):
        self._name = name

        if name == 'A':
            for x in range(4):
                blk = Block()
                blk.test_blue_plc_blk(x+1)
        elif name == 'B':
            for x in range(4):
                blk = Block()
                blk.test_blue_plc_blk(x+6)
        else:
            for x in range(4):
                blk = Block()
                blk.test_blue_plc_blk(x+11)



class Block(object):
    def __init__(self):
        self._number # block number inside line from plc file
        self._block_id # block id for internal use
        self._length # length of block in m
        self._speed_limit # speed limit inside block in km/hr
        self._station # station inside block if applicable
        self._occupied # indicates what train is occupying a block, 0 if unoccupied
        self._input_blocks = [] # indicates what blocks can input to this block
        self._output_blocks = [] # indicates what blocks this block can output to

    # hardcoded blue line function
    def test_blue_plc_blk(self, num):
        self._number = num
        self._length = 50
        self._speed_limit = 50
        if num == 10:
            B = Station()
            B.test_blue_plc_stat("B")
            self._station = B
        elif num == 15:
            C = Station()
            C.test_blue_plc_stat("C")
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


class Station(object):
    def __init__(self):
        self._name # name of station
        self._side # side of the track the station is on, 0 is left, 1 is right, 2 is both
    
    # hardcoded blue line function
    def test_blue_plc_stat(self, name):
        self._name = name


class Switch(object):
    def __init__(self):
        self._position # current position of the switch, corresponds with index of block_connections
        self._input_block # block feeding into the switch after which it forks
        self._block_connections = [] # output blocks
    
    # hardcoded blue line function
    def test_blue_plc_sw(self):
        self._position = 0
        self._input_block = 5
        self._block_connections.append(6)
        self._block_connections.append(11)


class Yard(object):
    def __init__(self):
        self._input_blocks = [] # blocks feeding into the yard
        self._output_blocks = [] # blocks where trains can leave the yard

    # hardcoded blue line function
    def test_blue_plc_yard(self):
        self._input_blocks.append(1)
        self._output_blocks.append(1)


class Train(object):
    def __init__(self):
        self._number # train id number
        self._authority # distance train is allowed to move in meters
        self._actual_velocity # actual velocity of train from train controller
        self._current_block = 0 # current position of train, 0 indicates yard
        self._schedule # object containing train's schedule
    
    # hardcoded blue line function
    def test_blue_plc_train(self, num):
        self._number = num


class Schedule(object):
    def __init__(self):
        self._arrival_time # train arrival time from dispatcher
        self._destination_station # train destination from dispatcher
        self._departure_time # calculated train departure time
        self._commanded_velocity # calculated velocity