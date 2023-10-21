import unittest
from datetime import datetime
from typing import Dict, Tuple
from unittest.mock import MagicMock, mock_open, patch

from src.pyDiagnostic import Diagnostic


class TestDiagnostic(unittest.TestCase):
    """
    Unit test for the Diagnostic class.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.
        """
        self.diagnostic = Diagnostic()
        self.events: Dict[str, Tuple[int, int, int, str]] = {
            "debug": (10, 1, 1, "This is a debug event"),
            "info": (20, 1, 1, "This is a info event"),
            "warning": (30, 1, 1, "This is a warning event"),
            "error": (40, 1, 1, "This is a error event"),
            "critical": (50, 1, 1, "This is a critical event"),
        }

    def test_set_event_status(self) -> None:
        """
        Test the set_event_status method.
        """
        self.diagnostic.set_event_status(self.events["debug"])
        self.assertFalse(
            self.diagnostic.events,
            "Assert for debug event should be False. DTC level is warning.",
        )

        self.diagnostic.set_event_status(self.events["info"])
        self.assertFalse(
            self.diagnostic.events,
            "Assert for info event should be False. DTC level is warning.",
        )

        self.diagnostic.set_event_status(self.events["warning"])
        self.assertEqual(
            self.diagnostic.events[-1][1:],
            self.events["warning"],
            "Assert for warning event should be True. DTC level is warning.",
        )

        self.diagnostic.set_event_status(self.events["error"])
        self.assertEqual(
            self.diagnostic.last_event[1:],
            self.events["error"],
            "Assert for error event should be True. DTC level is warning.",
        )

        self.diagnostic.set_event_status(self.events["critical"])
        self.assertEqual(
            self.diagnostic.last_event[1:],
            self.events["critical"],
            "Assert for critical event should be True. DTC level is warning.",
        )

    def test_look_up(self) -> None:
        """
        Test the look_up method.
        """
        for key, value in self.events.items():
            self.diagnostic.set_event_status(value)
            if key in ["debug", "info"]:
                self.assertFalse(self.diagnostic.look_up(value))
            else:
                self.assertTrue(self.diagnostic.look_up(value))

    def test_clean_up(self) -> None:
        """
        Test the clean_up method.
        """
        for key, value in self.events.items():
            self.diagnostic.set_event_status(value)
            if key in ["debug", "info"]:
                self.assertFalse(self.diagnostic.look_up(value))
            else:
                self.assertTrue(self.diagnostic.clean_up(value))
                self.assertFalse(self.diagnostic.look_up(value))

    def test_clear_DTC(self):
        self.diagnostic.set_event_status(self.events["critical"])
        self.diagnostic.clear_DTC()
        self.assertEqual(self.diagnostic.events, [])

    @patch("builtins.open", new_callable=mock_open)
    def test_dump_DTC(self, mock_file):
        self.diagnostic.set_event_status(self.events["critical"])
        self.diagnostic.dump_DTC()
        mock_file.assert_called_once_with("./log/DTC.log", "a")
        mock_file().write.assert_called_once()

    def test_last_event(self):
        self.diagnostic.set_event_status(self.events["error"])
        self.assertEqual(
            self.diagnostic.last_event, (str(datetime.now()), *self.events["error"])
        )

