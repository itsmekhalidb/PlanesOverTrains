class TrainModelTrainControllerAPI:
    def __init__(self) -> None:
        ''' Define variables passed between Train Model and Train Controller '''

        # From Train Model to Train Controller
        ## Track Model Information
        self.line = ""
        self.beacon = ""
        self.authority = 0
        self.cmd_speed = 0
        self.speed_limit = 0
        self.underground = False
        self.station_side = ""
        self.time = 0
        self.train_ids = {} # keys must be train ids

        ## Failure Information
        self.signal_pickup_failure = False
        self.engine_failure = False
        self.brake_failure = False
        self.ebrake_failure = False

        ## Train Information
        self.actual_velocity = 0
        self.temperature = 0

        # From Train Controller to Train Model
        self.cmd_power = 0.0
        self.emergency_brake = False
        self.service_brake_value = 0.0
        self.left_doors = False
        self.right_doors = False
        self.int_lights = False
        self.ext_lights = False
        self.temp_sp = 0.0
