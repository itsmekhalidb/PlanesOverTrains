from api.track_model_train_model_api import TrackModelTrainModelAPI
from track_model.block_info import block_info


class TrackControllerTrackModelAPI:
    def __init__(self) -> None:
        # Define variable passed between Track Controller and Track Model
        self._train_out = {}  # dispatched trains train id : [authority, commanded speed]
        self._train_in = {}  # train id : [actual velocity, occupancy, cum_distance]
        self._train_ids = set()  # train ids
        self._train_occupancy = list()
        self._line = "green"  # line
        self._commanded_speed = 0  # commanded speed
        self._time = 0
        self._track_info = {}
        self._occupancy = {"Green": [], "Red": []}
        # 1 = red, 0 = green
        self._lights = {"Green": {'1': 0, '13': 0, '28': 0, '150': 0, "62": 0, "76": 0, "77": 0, "85": 0,
                                  "100": 0},
                        "Red": {'1': 0, '15': 0, '16': 0, '10': 0, '76': 0, '72': 0, '71': 0,
                                '67': 0, '52': 0, '53': 0, '66': 0}}
        # 1 = left, 0 = right
        self._switches = {"Green": {'13': 0, '28': 0, '57': 0, '63': 0, '77': 0, '85': 0},
                          "Red": {'16': 0, '9': 0, '27': 0, '33': 0, '38': 0, '44': 0, '52': 0}}
        # crossing lights/gate
        self._railway_crossing = {"Green": {'18': 0},
                                  "Red": {'47': 0}}
        self._filepath = ""
        self.block_info = {}