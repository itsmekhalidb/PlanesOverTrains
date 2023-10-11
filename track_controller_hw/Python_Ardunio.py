import serial
import time

""""
ard = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

end = 1
while end == 1:
    output = str(ard.readline().decode('utf-8').strip())
    print(output)
    if output == "Button Pressed":
        ard.write("One".encode('utf-8'))

"""


class Hello(object):
    def __init__(self):
        self._blue = {'A1': {1: 50, 2: 0}, 'A2': {1: 50, 2: 0}, 'A3': {1: 50, 2: 0}, 'A4': {1: 50, 2: 0},
                      'A5': {1: 50, 2: 0}, 'B6': {1: 50, 2: 0}, 'B7': {1: 50, 2: 0}, 'B8': {1: 50, 2: 0},
                      'B9': {1: 50, 2: 0}, 'B10': {1: 50, 2: 0}, 'C11': {1: 50, 2: 0}, 'C12': {1: 50, 2: 0},
                      'C13': {1: 50, 2: 0}, 'C14': {1: 50, 2: 0}, 'C15': {1: 50, 2: 0}}
        self._switches = {'A5': 0, 'B6': 0, 'C11': 0}

    def get_occupancy(self, block) -> int:
        return self._blue[block][2]

    def set_occupancy(self, block, value: int):
        self._blue[block][2] = value

    def get_speed_limit(self, block) -> float:
        return self._blue[block][1]

    def set_speed_limit(self, block, value: float):
        self._blue[block][1] = value

    def set_speed_limit(self, block, value: float):
        self._blue[block][1] = value

    def get_switch(self, switch) -> int:
        return self._switches[switch]

    def set_switch(self, switch, value: int):
        self._switches[switch] = value


i = Hello()

print(i.get_switch('B6'))
i.set_switch('B6',1)
print(i.get_switch('B6'))
