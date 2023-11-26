import sys
import os
import unittest
from train_controller.train_controller import TrainController
from api.train_model_train_controller_api import TrainModelTrainControllerAPI as TrainSignals

class TrainControllerUnitTests(unittest.TestCase):

    def testBeacon(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        # Test set_beacon and get_beacon
        beacon_name = "Unit Test Station"
        tc.set_beacon(beacon_name)
        self.assertEqual(tc.get_beacon(), beacon_name)
    def test_set_temperature_sp(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        test_temp_sp = 25  # Example temperature setpoint
        tc.set_temperature_sp(test_temp_sp)
        self.assertEqual(tc.get_temperature_sp(), test_temp_sp, "Temperature setpoint not set correctly")


if __name__ == "__main__":
    unittest.main()
