import sys
import os
import unittest
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from CTC import CTC
from CTC import CTC_UI
from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.ctc_track_model_api import CTCTrackModelAPI

class CTCUnitTests(unittest.TestCase):
    def test_block_maintenance_mode(self):
        ctc_tc_signals = CTCTrackControllerAPI
        ctc_tm_signals = CTCTrackModelAPI
        ctc = CTC(ctc_tc_signals, ctc_tm_signals)
        ctc.change_block("A1")
        self.assertTrue("A1" in ctc_tc_signals._track_section_status)
    
    def test_green_dispatch(self):
        ctc_tc_signals = CTCTrackControllerAPI
        ctc_tm_signals = CTCTrackModelAPI
        ctc = CTC(ctc_tc_signals, ctc_tm_signals)
        t = datetime(year=2023, month=12, day=13, hour=7, minute=1, second=3)
        ctc.create_schedule(65, 0, "Glenbury", t, "green", ctc_tc_signals)
        self.assertTrue(len(ctc._trains) == 1)

    def test_red_dispatch(self):
        ctc_tc_signals = CTCTrackControllerAPI
        ctc_tm_signals = CTCTrackModelAPI
        ctc = CTC(ctc_tc_signals, ctc_tm_signals)
        t = datetime(year=2023, month=12, day=13, hour=7, minute=1, second=3)
        ctc.create_schedule(7, 0, "Shadyside", t, "red", ctc_tc_signals)
        self.assertTrue(len(ctc._trains) == 1)

if __name__ == "__main__":
    unittest.main()