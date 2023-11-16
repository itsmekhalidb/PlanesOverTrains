class CTCTrackModelAPI:
    def __init__(self) -> None:
        # define variable to pass between CTC and Track Model
        self._ticket_sales = {} # {train id : number tickets}