# Imports
import time

# Constants
MAX_POWER = 120000

class Controller:

    '''
    Forward Euler Method:
    This method is best for small sampling times, where the Nyquist limit is large compared to the bandwidth of the
    controller. For larger sampling times, the Forward Euler method can result in instability, even when discretizing a
    system that is stable in continuous time.
    '''

    def __init__(self, system_time) -> None:
        # Time Variables
        self._time = system_time
        self._current_time = self._time
        self._previous_time = self._time
        # Gains
        self._kp = 0.0
        self._ki = 0.0
        # Error Terms
        self._uk = 0.0
        self._ek = 0.0
        self._previous_error = 0.0
        # Helper Variables
        self._i_term = 0.0
        self._p_term = 0.0

    def set_gains(self, kp: float, ki: float):
        self._kp = kp
        self._ki = ki

    def update(self, current_velocity: float, commanded_velocity: float):
        # Update current time to now
        self._current_time = self._time

        # Get dt
        change_time = self._current_time.timestamp() - self._previous_time.timestamp()

        # Get error
        self._ek = commanded_velocity - current_velocity

        # Get error change by time
        error = self._ek * change_time

        # Kp * Ek
        self._p_term = self._kp * self._ek

        # Increment I term if it is less than max power
        if self._i_term + error <= MAX_POWER:
            self._i_term += error

        # Update previous time
        self._previous_time = self._current_time

        # Return calculated power
        return self._p_term + self._ki * self._i_term

