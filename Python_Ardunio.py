import pyfirmata
import time

board = pyfirmata.Arduino("COM5");

board.digital[8].write(1)
time.sleep(1)
board.digital[8].write(0)
time.sleep(1)
