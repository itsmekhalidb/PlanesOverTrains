import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from track_controller.track_controller import Track_Controller
from api.ctc_track_controller_api import CTCTrackControllerAPI as CTCSignals
from api.track_controller_track_model_api import TrackControllerTrackModelAPI as TrackSignals

class TrackModelUnitTests(unittest.TestCase):
    def test_occupancy(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_occupancy('6', 1)
        self.assertEqual(tc.get_occupancy('6'), 1)
        tc.set_occupancy('6', 0)
        self.assertEqual(tc.get_occupancy('6'), 0)

    def test_switches(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_switch('13', 1)
        self.assertEqual(tc.get_switch('13'), 1)
        tc.set_switch('29', 0)
        self.assertEqual(tc.get_switch('29'), 0)

    def test_lights(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_lights('150', 1)
        self.assertEqual(tc.get_light('150'), 1)
        tc.set_lights('150', 0)
        self.assertEqual(tc.get_light('150'), 0)

    def test_track_status(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_track_section_status({'23' : 1})
        self.assertEqual(tc.get_occupancy('23'), 1)
        tc.set_track_section_status({'23' : 0})
        self.assertEqual(tc.get_occupancy('23'), 0)

    def test_railway_crossing(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_railway_crossing('18', 1)
        self.assertEqual(tc.get_railway_crossing('18'), 1)
        tc.set_railway_crossing('18', 0)
        self.assertEqual(tc.get_railway_crossing('18'), 0)

    def test_authority(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_train_out({1 : [50, 0]})
        self.assertEqual(tc.get_authority(1), 50)
        tc.set_authority(1, 20)
        self.assertEqual(tc.get_authority(1), 20)

if __name__ == "__main__":
    unittest.main()