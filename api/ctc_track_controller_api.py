from datetime import datetime
from track_model.block_info import block_info

class CTCTrackControllerAPI:
    def __init__(self) -> None:
        # Define variables passed between CTC and Track Controller

        #CTC to Track Controller
        self._train_info = {} # train id : [[authority] : suggested speed]
        self._track_section_status = [] # blocks, in list is closed, not in list is open
        self._suggested_speed = 0.0 # meters/sec
        self._commanded_speed = {'A1': 0} # train: commanded speed in m/s
        # self._time = datetime.combine(datetime.now().date(), datetime.min.time()) # current time
        self._time = 0 # current time

        #Track Controller to CTC
        self._curr_speed = {}
        self._passenger_onboarding = 0 # tickets sold
        self._occupancy = {'A1': 0} # blocks{occupancy(bool)}
        self._light = ("light color", 0) # light color, color (0 for green, 1 for red)
        self._switch = (0, 0) # switch position (first is switch number, second is position)
        self._green_cutoffs = {"Green 1" : ['A1::I52', 'W127::Z150'], "Green 2" : ['I53::W126']}
        self._track_info = {}
        # Block Data, 1 = Speed Limit, 2 = Occupancy, 3 = light, 4 = switch, 5 = gate/crossing
        self._blue = {'A1': {1: 50, 2: 1, 3: 0, 4: 0, 5: 0}, 'A2': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}, 'A3': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0},
                      'A4': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}, 'A5': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}, 'B6': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0},
                      'B7': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}, 'B8': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0},'B9': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0},
                      'B10': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}, 'C11': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}, 'C12': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0},
                      'C13': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}, 'C14': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}, 'C15': {1: 50, 2: 0, 3: 0, 4: 0, 5: 0}}

        self._green = {'A1': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'A2': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'A3': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'B4': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'B5': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'B6': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'C7': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'C8': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'C9': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'C10': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'C11': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'C12': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'D13': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'D14': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'D15': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'D16': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'E17': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'E18': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'E19': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'E20': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'F21': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'F22': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'F23': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'F24': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'F25': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'F26': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'F27': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'F28': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'G29': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'G30': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'G31': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'G32': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'H33': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'H34': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'H35': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I36': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'I37': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I38': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I39': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'I40': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I41': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I42': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'I43': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I44': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I45': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'I46': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I47': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I48': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'I49': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I50': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I51': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'I52': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I53': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I54': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'I55': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I56': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'I57': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'J58': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'J59': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'J60': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'J61': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'J62': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'K63': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'K64': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'K65': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'K66': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'K67': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'K68': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'L69': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'L70': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'L71': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'L72': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'L73': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'M74': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'M75': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'M76': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'N77': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'N78': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'N79': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'N80': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'N81': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'N82': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'N83': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'N84': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'N85': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'O86': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'O87': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'O88': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'P89': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'P90': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'P91': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'P92': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'P93': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'P94': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'P95': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'P96': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'P97': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'Q98': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'Q99': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'Q100': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'R101': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'S102': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'S103': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'S104': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'T105': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'T106': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'T107': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'T108': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'T109': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'U110': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'U111': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'U112': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'U113': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'U114': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'U115': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'U116': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'V117': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'V118': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'V119': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'V120': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'V121': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W122': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W123': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'W124': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W125': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W126': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'W127': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W128': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W129': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'W130': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W131': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W132': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'W134': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W135': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W136': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'W137': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W138': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W139': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'W140': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W141': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'W142': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'W143': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'X144': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'X145': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'X146': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'Y147': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'Y148': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
                       'Y149': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'Z150': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
                       }

