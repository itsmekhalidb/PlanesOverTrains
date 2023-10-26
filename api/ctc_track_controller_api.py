class CTCTrackControllerAPI:
    def __init__(self) -> None:
        # Define variable passed between CTC and Track Controller\

        #CTC to Track Controller
        self._authority = 0.0 # meters
        self._track_section_status = {'A1': False} #blocks{track status(bool)}
        self._suggested_speed = 0.0 # meters/sec

        #Track Controller to CTC
        self._passenger_onboarding = 0 # tickets sold
        self._occupancy = {'A1': 0} # blocks{occupancy(bool)}
        self._light = ("light color", 0) # light color, color (0 for green, 1 for red)
        self._switch = (0, 0) # switch position (first is switch number, second is position)

