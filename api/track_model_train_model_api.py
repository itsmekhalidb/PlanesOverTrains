from track_model.block_info import block_info

class TrackModelTrainModelAPI:
    def __init__(self) -> None:
        ''' Define variables passed between Train Model and Track Model '''

        # From Train Model to Track Model
        self.passenger_departing = 0
        self.passenger_onboard = 0
        self.actual_velocity = 0.0

        # From Track Model to Train Model
        self.line = ""
        self.authority = 0.0
        self.cmd_speed = 0.0
        self.time = 0
        self.filepath = ""
        self.track_info = block_info(self.filepath)
        self.current_block = 0
