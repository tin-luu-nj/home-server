import unittest
from datetime import datetime
from typing import Dict, Tuple
from unittest.mock import MagicMock, mock_open, patch

from src.pyDiagnostic import Diagnostic


class TestDiagnosticHandler(unittest.TestCase):
    """
    Unit test for the Diagnostic class.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.
        """
        self.diagnostic = Diagnostic()
        self.events: Dict[str, Tuple[int, int, int, str]] = {
            "critical": (50, 1, 1, "This is a critical event"),
        }

    @patch("logging.StreamHandler.emit")
    @patch("logging.FileHandler.emit")
    def test_logging_handling(self, mock_StreamHandler_emit, mock_FileHandler_emit):
        self.diagnostic.set_event_status(self.events["critical"])
        # Call emit twice, one for LogRecord, once for FileHandler
        mock_StreamHandler_emit.assert_called()
        mock_FileHandler_emit.assert_called()

