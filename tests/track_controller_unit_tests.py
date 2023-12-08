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
        tc.set_switch("Green", '13', 1)
        self.assertEqual(tc.get_switch("Green", '13'), 1)
        tc.set_switch("Green", '29', 0)
        self.assertEqual(tc.get_switch("Green", '29'), 0)

    def test_lights(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_lights("Green", '150', 1)
        self.assertEqual(tc.get_light("Green", '150'), 1)
        tc.set_lights("Green", '150', 0)
        self.assertEqual(tc.get_light("Green", '150'), 0)

    def test_track_status(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_track_section_status({'23': 1})
        self.assertEqual(tc.get_occupancy('23'), 1)
        tc.set_track_section_status({'23': 0})
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
        tc.set_train_out({1: [50, 0]})
        self.assertEqual(tc.get_authority(1), 50)
        tc.set_authority(1, 20)
        self.assertEqual(tc.get_authority(1), 20)

    def test_plc(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_occupancy('13', 1)
        f = open("../track_controller/PLCgreen1.txt", "r")
        lines = f.readlines()
        i = 0
        while i < len(lines) - 1:
            if lines[i].strip() != "switch" and lines[i].strip() != "light":
                if tc.get_operator() == "switch":
                    tc.set_switch("Green", str(lines[i].strip()),
                                  tc.parse(lines[i + 1].strip()))
                elif tc.get_operator() == "light":
                    tc.set_lights("Green", str(lines[i].strip()),
                                  tc.parse(lines[i + 1].strip()))
                i = i + 1
            else:
                tc.set_operator(lines[i].strip())
            i = i + 1

        self.assertEqual(tc.get_switch("Green", '28'), 1)
        f.close()


if __name__ == "__main__":
    unittest.main()
