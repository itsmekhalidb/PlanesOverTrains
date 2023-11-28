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


if __name__ == "__main__":
    unittest.main()