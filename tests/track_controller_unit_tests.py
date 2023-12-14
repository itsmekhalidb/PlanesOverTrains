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
        tc.set_occupancy("Green",'6', 1)
        self.assertEqual(tc.get_occupancy("Green",'6'), 1)
        tc.set_occupancy("Green",'6', 0)
        self.assertEqual(tc.get_occupancy("Green",'6'), 0)

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
        tc.set_track_section_status({"Green": {'23': 1}, "Red": {}})
        self.assertEqual(tc.get_occupancy("Green",'23'), 1)
        tc.set_track_section_status({"Green": {'23': 0}, "Red": {}})
        self.assertEqual(tc.get_occupancy("Green", '23'), 0)

    def test_railway_crossing(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_railway_crossing("Green",'18', 1)
        self.assertEqual(tc.get_railway_crossing("Green",'18'), 1)
        tc.set_railway_crossing("Green",'18', 0)
        self.assertEqual(tc.get_railway_crossing("Green",'18'), 0)

    def test_authority(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_train_out({1: [50, 0]})
        self.assertEqual(tc.get_authority(1), 50)
        tc.set_authority(1, 20)
        self.assertEqual(tc.get_authority(1), 20)

    def test_green1_plc(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_occupancy("Green",'13', 1)
        f = open("../track_controller/PLCgreen1.txt", "r")
        lines = f.readlines()
        i = 0
        while i < len(lines) - 1:
            if lines[i].strip() != "switch" and lines[i].strip() != "light" and lines[i].strip() != "railway":
                if tc.get_operator() == "switch":
                    tc.set_switch("Green", str(lines[i].strip()),
                                  tc.parse(lines[i + 1].strip(), "Green"))
                elif tc.get_operator() == "light":
                    tc.set_lights("Green", str(lines[i].strip()),
                                  tc.parse(lines[i + 1].strip(), "Green"))
                i = i + 1
            else:
                tc.set_operator(lines[i].strip())
            i = i + 1

        self.assertEqual(tc.get_switch("Green", '28'), 1)
        f.close()

    def test_red1_plc_switch(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_occupancy("Red", '1', 1)
        f = open("../track_controller/PLCred1.txt", "r")
        lines = f.readlines()
        i = 0
        while i < len(lines) - 1:
            if lines[i].strip() != "switch" and lines[i].strip() != "light" and lines[i].strip() != "railway":
                if tc.get_operator() == "switch":
                    tc.set_switch("Red", str(lines[i].strip()),
                                                     tc.parse(lines[i + 1].strip(), "Red"))
                elif tc.get_operator() == "light":
                    tc.set_lights("Red", str(lines[i].strip()),
                                                     tc.parse(lines[i + 1].strip(), "Red"))
                elif tc.get_operator() == "railway":
                    tc.set_railway_crossing("Red", str(lines[i].strip()),
                                            tc.parse(lines[i + 1].strip(), "Red"))
                i = i + 1
            else:
                tc.set_operator(lines[i].strip())
            i = i + 1
        self.assertEqual(tc.get_switch("Red", '16'), 1)
        f.close()

    def test_red1_plc_light(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_occupancy("Red", '27', 1)
        f = open("../track_controller/PLCred1.txt", "r")
        lines = f.readlines()
        i = 0
        while i < len(lines) - 1:
            if lines[i].strip() != "switch" and lines[i].strip() != "light" and lines[i].strip() != "railway":
                if tc.get_operator() == "switch":
                    tc.set_switch("Red", str(lines[i].strip()),
                                                     tc.parse(lines[i + 1].strip(), "Red"))
                elif tc.get_operator() == "light":
                    tc.set_lights("Red", str(lines[i].strip()),
                                                     tc.parse(lines[i + 1].strip(), "Red"))
                elif tc.get_operator() == "railway":
                    tc.set_railway_crossing("Red", str(lines[i].strip()),
                                            tc.parse(lines[i + 1].strip(), "Red"))
                i = i + 1
            else:
                tc.set_operator(lines[i].strip())
            i = i + 1
        self.assertEqual(tc.get_light("Red", '76'), 0)
        f.close()

    def test_red2_plc(self):
        ctc_cigs = CTCSignals()
        track_cigs = TrackSignals()
        tc = Track_Controller(ctcsignals=ctc_cigs, tracksignals=track_cigs)
        tc.set_occupancy("Red", '38', 1)
        f = open("../track_controller/PLCred2.txt", "r")
        lines = f.readlines()
        i = 0
        while i < len(lines) - 1:
            if lines[i].strip() != "switch" and lines[i].strip() != "light" and lines[i].strip() != "railway":
                if tc.get_operator() == "switch":
                    tc.set_switch("Red", str(lines[i].strip()),
                                                     tc.parse(lines[i + 1].strip(), "Red"))
                elif tc.get_operator() == "light":
                    tc.set_lights("Red", str(lines[i].strip()),
                                                     tc.parse(lines[i + 1].strip(), "Red"))
                elif tc.get_operator() == "railway":
                    tc.set_railway_crossing("Red", str(lines[i].strip()),
                                            tc.parse(lines[i + 1].strip(), "Red"))
                i = i + 1
            else:
                tc.set_operator(lines[i].strip())
            i = i + 1
        self.assertEqual(tc.get_switch("Red", '38'), 1)
        f.close()




if __name__ == "__main__":
    unittest.main()
