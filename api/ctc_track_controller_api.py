from datetime import datetime
from track_model.block_info import block_info

class CTCTrackControllerAPI:
    def __init__(self) -> None:
        # Define variables passed between CTC and Track Controller

        #CTC to Track Controller
        self._train_out = {} # dispatched trains train id : [authority, commanded speed]
        self._track_section_status = {} # blocks: status 1 is closed, 0 is open
        self._maintenance_switch = [{}, {}] # green, red lines with {switch name: position}
        self._suggested_speed = 0 # meters/sec
        self._commanded_speed = {'A1': 0} # train: commanded speed in m/s
        # self._time = datetime.combine(datetime.now().date(), datetime.min.time()) # current time
        self._time = 0 # current time

        #Track Controller to CTC
        self._train_ids = set() # train ids
        self._train_in = {}  # train id : [actual velocity (m/s), occupied block, cum_distance]
        self._curr_speed = {}
        self._passenger_onboarding = 0 # tickets sold
        self._occupancy = {} # trains and their occupied blocks
        # 1 = red, 0 = green
        self._light = {"Green": {'1': 0, '13': 0, '28': 0, '150': 0, "62": 0, "76": 0, "77": 0, "85": 0,
                                  "100": 0},
                        "Red": {'1': 0, '15': 0, '16': 0, '10': 0, '76': 0, '72': 0, '71': 0,
                                '67': 0, '52': 0, '53': 0, '66': 0}}
        # 1 = left, 0 = right
        self._switch = {"Green": {'13': 0, '28': 0, '57': 0, '63': 0, '77': 0, '85': 0},
                          "Red": {'16': 0, '9': 0, '27': 0, '33': 0, '38': 0, '44': 0, '52': 0}}
        self._green_cutoffs = {"Green 1" : ['A1::I52', 'W127::Z150'], "Green 2" : ['I53::W126']}
        self._filepath = ""
        self._track_info = {}


