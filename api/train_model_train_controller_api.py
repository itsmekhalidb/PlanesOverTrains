class TrainModelTrainControllerAPI:
    def __init__(self) -> None:
        # Define variable passed between Train Model and Train Controller

        # From Train Model to Train Controller
        self.beacon = "" # track model
        self.authority = 0 # track model
        self.cmd_speed = 0 # track model
        self.speed_limit = 0 # track model
        self.underground = False # track model
        self.station_side = "" # track model

        self.signal_pickup_failure = False
        self.engine_failure = False
        self.brake_failure = False
        self.ebrake_failure = False

        self.time = 0
        self.actual_velocity = 0

        # From Train Controller to Train Model
        self.cmd_power = 0.0
        self.emergency_brake = False
        # self.service_brake = False
        self.service_brake_value = 0.0
        self.left_doors = False
        self.right_doors = False
        self.int_lights = False
        self.ext_lights = False
        self.temp_sp = 0.0
        self.temperature = 0
