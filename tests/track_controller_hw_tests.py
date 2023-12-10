import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from track_controller_hw.track_controller_hw import Track_Controller_HW
from api.ctc_track_controller_api import CTCTrackControllerAPI as CTCSignals
from api.track_controller_track_model_api import TrackControllerTrackModelAPI as TrackSignals

class TrackControllerHWUnitTests(unittest.TestCase):
    def test_occupancy(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller_HW(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_occupancy('6', 1)
        self.assertEqual(tc.get_occupancy('6'), 1)
        tc.set_occupancy('6', 0)
        self.assertEqual(tc.get_occupancy('6'), 0)

    def test_track_status(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller_HW(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_track_section_status({'23': 1})
        self.assertEqual(tc.get_occupancy('23'), 1)
        tc.set_track_section_status({'23': 0})
        self.assertEqual(tc.get_occupancy('23'), 0)

    def test_switches(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller_HW(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_switch('D13', 1)
        self.assertEqual(tc.get_switch('D13'), 1)
        tc.set_switch('F28', 0)
        self.assertEqual(tc.get_switch('F28'), 0)

    def test_lights(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller_HW(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_lights('Z150', 1)
        self.assertEqual(tc.get_lights('Z150'), 1)
        tc.set_lights('Z150', 0)
        self.assertEqual(tc.get_lights('Z150'), 0)

    def test_plc_parser(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller_HW(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        string = tc.get_plc_logic().parse()
        self.assertEqual(string, "DFaZ0 EFaz0")

if __name__ == "__main__":
    unittest.main()