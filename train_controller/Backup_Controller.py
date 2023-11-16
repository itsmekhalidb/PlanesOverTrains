import time
from .Controller import Controller, MAX_POWER



class Backup_Controller(Controller):

        '''
        Trapezoidal Rule PI Controller:
        An advantage of the Trapezoidal method is that discretizing a stable continuous-time system using this method
        always yields a stable discrete-time result. Of all available integration methods, the Trapezoidal method yields
        the closest match between frequency-domain properties of the discretized system and the corresponding
        continuous-time system.
        '''

        def __int__(self,system_time) -> None:
            super().__init__(system_time=system_time)

        def update(self, current_velocity: float, commanded_velocity: float) -> float:
            # Update current time to now
            self._current_time = self._time
            # Get dt
            change_time = self._current_time - self._previous_time
            # Get error
            error = commanded_velocity - current_velocity
            # Kp * Ek
            self._p_term = self._kp * error
            # Get error change by time
            error_rate = (change_time/2)*(error + self._previous_error)
            # Increment I term if it is less than max power
            if self._i_term + error_rate <= MAX_POWER:
                self._i_term += error_rate
            # Update previous time
            self._previous_error = error
            # Set previous time to current time
            self._previous_time = self._current_time
            # Return calculated power
            return self._p_term + self._ki * self._i_term

