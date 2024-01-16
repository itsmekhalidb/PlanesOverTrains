import sys
import os
import unittest
from train_controller.train_controller import TrainController
from api.train_model_train_controller_api import TrainModelTrainControllerAPI as TrainSignals

class TrainControllerUnitTests(unittest.TestCase):

    def test_PI_Controller_Output(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        # Test PI_Controller_Output
        tc.set_authority(50)
        tc._backup_controller.set_gains(8000, 10)
        tc._controller.set_gains(7999, 10)
        if tc._backup_controller.update(24, 50) != tc._controller.update(20, 50):
            tc.set_power()
        self.assertEqual(tc.set_power(), 0, "Power not set correctly")
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
    def test_ebrake(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        tc.set_service_brake_failure(True)
        tc.set_signal_pickup_failure_status(True)
        tc.set_power()
        self.assertEqual(tc.get_ebrake_status(), True, "Ebrake not set correctly")

    def test_power_goes_low(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        tc.set_service_brake_failure(True)
        tc.set_signal_pickup_failure_status(True)
        tc.set_power()
        self.assertEqual(tc.set_power(), 0, "Power not set correctly")

    def test_doors_in_manual_mode(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        tc.set_auto_status(False)
        tc.set_right_door_status(True)
        tc.set_left_door_status(True)
        self.assertEqual(tc.get_right_door_status(), True, "Doors not in manual mode")
        self.assertEqual(tc.get_left_door_status(), True, "Doors not in manual mode")

    def test_lights_on_undergound(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        #tm = TrainModel(tran_model_api=train_sigs)
        tc.set_auto_status(False)
        tc.set_underground_status(True)
        tc.set_time(23)
        tc.set_external_lights()
        tc.set_internal_lights()
        self.assertEqual(tc.get_external_lights(), True, "Lights not in manual mode")
        self.assertEqual(tc.get_internal_lights(), True, "Lights not in manual mode")

    def test_lights_manual_mode(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        tc.set_auto_status(False)
        tc.set_underground_status(False)
        tc.set_external_lights()
        tc.set_internal_lights()
        self.assertEqual(tc.get_external_lights(), True, "Lights not in manual mode")
        self.assertEqual(tc.get_internal_lights(), True, "Lights not in manual mode")

    def test_train_stops_at_station(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        tc.set_next_station("Dormont")
        tc.set_authority(50)
        tc.set_commanded_velocity(30)
        tc.set_authority(0)
        tc._side = "Right"
        tc.set_station_side()
        self.assertEqual(tc.get_right_door_status(), True, "Train did not stop at station")
        self.assertEqual(tc.get_next_station(), "Dormont", "Train did not stop at station")

    def test_brakes_based_on_authority(self):
        train_sigs = TrainSignals()
        tc = TrainController(train_model_api=train_sigs)
        tc.set_next_station("Dormont")
        tc.set_commanded_velocity(30)
        tc.set_authority(0)
        self._stop = False
        tc.set_power()
        self.assertEqual(tc.set_power(), 0, "Power not set correctly")
        self.assertEqual((tc.get_service_brake_value())>0, True, "Brakes not set correctly")



if __name__ == "__main__":
    unittest.main()
