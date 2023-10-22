import pytest
from datetime import datetime
from typing import Dict, Tuple
from unittest.mock import mock_open, patch

from src.pyDiagnostic import Diagnostic


# Set up the test environment.
@pytest.fixture
def diagnostic():
    events: Dict[str, Tuple[int, int, int, str]] = {
        "debug": (10, 1, 1, "This is a debug event"),
        "info": (20, 1, 1, "This is a info event"),
        "warning": (30, 1, 1, "This is a warning event"),
        "error": (40, 1, 1, "This is a error event"),
        "critical": (50, 1, 1, "This is a critical event"),
    }
    return Diagnostic(), events


@patch("logging.StreamHandler.emit")
@patch("logging.FileHandler.emit")
def test_logging_handling(mock_StreamHandler_emit, mock_FileHandler_emit, diagnostic):
    diagnostic_obj, events = diagnostic
    diagnostic_obj.set_event_status(events["critical"])
    # Call emit twice, one for LogRecord, once for FileHandler
    mock_StreamHandler_emit.assert_called()
    mock_FileHandler_emit.assert_called()


def test_set_event_status(diagnostic):
    diagnostic_obj, events = diagnostic
    diagnostic_obj.set_event_status(events["debug"])
    assert not diagnostic_obj.events

    diagnostic_obj.set_event_status(events["info"])
    assert not diagnostic_obj.events

    diagnostic_obj.set_event_status(events["warning"])
    assert diagnostic_obj.events[-1][1:] == events["warning"]

    diagnostic_obj.set_event_status(events["error"])
    assert diagnostic_obj.last_event[1:] == events["error"]

    diagnostic_obj.set_event_status(events["critical"])
    assert diagnostic_obj.last_event[1:] == events["critical"]


def test_look_up(diagnostic):
    diagnostic_obj, events = diagnostic
    for key, value in events.items():
        diagnostic_obj.set_event_status(value)
        if key in ["debug", "info"]:
            assert not diagnostic_obj.look_up(value)
        else:
            assert diagnostic_obj.look_up(value)


def test_clean_up(diagnostic):
    diagnostic_obj, events = diagnostic
    for key, value in events.items():
        diagnostic_obj.set_event_status(value)
        if key in ["debug", "info"]:
            assert not diagnostic_obj.look_up(value)
        else:
            assert diagnostic_obj.clean_up(value)
            assert not diagnostic_obj.look_up(value)


def test_clear_DTC(diagnostic):
    diagnostic_obj, events = diagnostic
    diagnostic_obj.set_event_status(events["critical"])
    diagnostic_obj.clear_DTC()
    assert not diagnostic_obj.events


@patch("builtins.open", new_callable=mock_open)
def test_dump_DTC(mock_file, diagnostic):
    diagnostic_obj, events = diagnostic
    diagnostic_obj.set_event_status(events["critical"])
    diagnostic_obj.dump_DTC()
    mock_file.assert_called_once_with("./log/DTC.log", "a")
    mock_file().write.assert_called_once()


def test_last_event(diagnostic):
    diagnostic_obj, events = diagnostic
    diagnostic_obj.set_event_status(events["error"])
    assert (str(datetime.now()), *events["error"]) == diagnostic_obj.last_event
