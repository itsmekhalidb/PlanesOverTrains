class TrackModelTrainModelAPI:
    def __init__(self):
        ''' Define variables passed between Train Model and Track Model '''

        # From Train Model to Track Model
        self.passenger_departing = 0
        self.passenger_onboard = 0
        self.actual_velocity = 0.0

        # From Track Model to Train Model
        self.line = ""
        self.beacon = ""
        self.authority = 0
        self.cmd_speed = 0
        self.time = 0
        self.red_track_info = {}
        self.green_track_info = {}
        self.current_block = 0
