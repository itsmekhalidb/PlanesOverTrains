import sys
import os
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from CTC import CTC
from CTC import CTC_UI
from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.ctc_track_model_api import CTCTrackModelAPI

class CTCUnitTests(unittest.TestCase):
    def test_maintenance_mode(self):
        ctc_tc_signals = CTCTrackControllerAPI
        ctc_tm_signals = CTCTrackModelAPI
        ctc = CTC(ctc_tc_signals, ctc_tm_signals)
        ctc.change_block("A1")
        self.assertTrue("A1" in ctc_tc_signals._track_section_status)

if __name__ == "__main__":
    unittest.main()