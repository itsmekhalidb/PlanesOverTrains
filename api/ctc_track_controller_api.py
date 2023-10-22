class CTCTrackControllerAPI:
    def __init__(self):
        # Define variable passed between CTC and Track Controller\

        #CTC to Track Controller
        self._authority = 0.0 # meters
        self._track_section_status = {'block': False} #blocks{track status(bool)}
        self._suggested_speed = 0.0 # meters/sec

        #Track Controller to CTC
        self._passenger_onboarding = 0 # tickets sold
        self._occupancy = {'block': {1: 0.0, 2: False}} # blocks{speed limit(m/s), occupancy(bool)}

    def get_authority(self) -> float:
        return self._authority
    def get_track_section_status(self, block) -> bool:
        return self._track_section_status[block]

    def get_suggested_speed(self) -> float:
        return self._suggested_speed

    def get_passenger_onboarding(self) -> int:
        return self._passenger_onboarding

    def get_occupancy(self, block) -> bool:
        return self._occupancy[block][2]

    def set_authority(self, distance: float):
        self._authority = distance

    def set_track_section_status(self, block, mode: bool):
        self._track_section_status[block] = mode
        self._occupancy[block][2] = mode

    def set_suggested_speed(self, speed: float):
        self._suggested_speed = speed

    def set_passenger_onboarding(self, tickets: int):
        self._passenger_onboarding = tickets

    def set_occupancy(self, block, value: bool):
        self._occupancy[block][2] = value
