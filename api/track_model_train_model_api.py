class TrackModelTrainModelAPI:
    def __init__(self):
        ''' Define variables passed between Train Model and Track Model '''

        # From Train Model to Track Model
        self.passenger_departing = 0
        self.passenger_onboard = 0
        self.actual_velocity = 0.0
        self.signal_pickup_failure = False # Not sure if this is needed

        # From Track Model to Train Model
        self.line = ""
        self.beacon = ""
        self.authority = 0
        self.cmd_speed = 0
        # self.speed_limit = 0
        # self.underground = False
        # self.station_side = "" # Need input from Nadin on how to handle
        self.time = 0
        self.red_track_info = {} # Need input from Nadin on how to handle
        self.green_track_info = {} # Need input from Nadin on how to handle
        self.current_block = 0 # Need input from Nadin on how to handle