"""
This module contains the Inspector class for performing diagnostics.

Imports:
    logging: A module in Python Standard Library for event logging.
    datetime: A module in Python Standard Library for manipulating dates and times.
    Dict, Tuple: Typing constructs for annotating types of variables.
    Mock, mock_open, patch: Constructs from unittest.mock module for mocking objects in tests.
    pytest: A testing framework that allows you to write test codes using python.

Classes:
    Inspector: Describe the purpose and functionality of this class.
"""

import logging
from datetime import datetime
from typing import Dict, Tuple
from unittest.mock import Mock, mock_open, patch

import pytest

from src.pyDiagnostic import Inspector


@pytest.fixture
def diagnosing(
    monkeypatch,
) -> Tuple[Inspector, Dict[str, Tuple[int, int, int, str]], Mock]:
    """
    Pytest fixture for setting up the test environment.

    This fixture creates an instance of the 'Inspector' class and a dictionary of events.
    Each event is a tuple containing an integer and a string.

    Returns:
    Tuple[Inspector, Dict[str, Tuple[int, int, int, str]]]: A tuple containing an instance of 'Inspector' and a dictionary of events.
    """

    # Define the events
    events: Dict[str, Tuple[int, int, int, str]] = {
        "debug": (10, 1, 1, "Dummy debug event"),
        "info": (20, 1, 1, "Dummy info event"),
        "warning": (30, 1, 1, "Dummy warning event"),
        "error": (40, 1, 1, "Dummy error event"),
        "critical": (50, 1, 1, "Dummy critical event"),
    }

    mock_log = Mock()
    monkeypatch.setattr(logging.Logger, "_log", mock_log)

    # Return the 'Inspector' instance and the events
    return events, mock_log


def test_001_C_Inspector_B_logging_handling(
    diagnosing: Tuple[Dict[str, Tuple[int, int, int, str]], Mock]
) -> None:
    """
    Test the logging handling function.

    Args:
        monkeypatch (object): The monkeypatch fixture from pytest.
        diagnosing (Tuple[object, Dict[str, str]]): A tuple containing a test object and a dictionary of events.

    Returns:
        None
    """

    # Arrange
    _obj = Inspector(
        logger_name="test_001_C_Inspector_B_logging_handling",
        logger_level=logging.INFO,
        stream_handler_enable=True,
        file_handler_path="log/test_001_C_Inspector_B_logging_handling+DDX.log",
        file_handler_enable=True,
    )
    _events, _mock_log = diagnosing

    file_handlers = [
        h for h in _obj.logger.handlers if isinstance(h, logging.FileHandler)
    ]
    stream_handlers = [
        h for h in _obj.logger.handlers if isinstance(h, logging.StreamHandler)
    ]

    # Act
    _obj.set_event_status(_events["critical"])

    # Assert
    assert logging.INFO == _obj.logger.level
    assert logging.DEBUG == _obj.logger.handlers[0].level
    assert logging.DEBUG == _obj.logger.handlers[1].level
    assert 1 == len(file_handlers)
    assert 2 == len(stream_handlers)
    assert 1 == _mock_log.call_count
    _mock_log.assert_called_once_with(50, "Dummy critical event", ())


def test_002_C_Inspector_M_set_event_status(
    diagnosing: Tuple[Dict[str, Tuple[int, int, int, str]], Mock]
) -> None:
    """
    Test the set_event_status method of a diagnosing object.

    Args:
        monkeypatch: The pytest fixture for safely mocking attributes.
        diagnosing (Tuple[Any, Dict[str, str]]): A tuple containing a diagnosing object and an events dictionary.

    Raises:
        AssertionError: If the set_event_status method does not behave as expected.
    """
    # Arrange
    _obj = Inspector(
        logger_name="test_002_C_Inspector_M_set_event_status",
        logger_level=logging.INFO,
        stream_handler_enable=True,
        file_handler_enable=True,
        dtc_level=logging.WARNING,
    )
    _events, _ = diagnosing

    # Act & Assert for "debug" event
    _obj.set_event_status(_events["debug"])
    assert not _obj.events, "Events should be empty after setting debug status"

    # Act & Assert for "info" event
    _obj.set_event_status(_events["info"])
    assert not _obj.events, "Events should be empty after setting info status"

    # Act & Assert for "warning" event
    _obj.set_event_status(_events["warning"])
    assert _obj.events[-1][1:] == _events["warning"], "Last event should be warning"

    # Act & Assert for "error" event
    _obj.set_event_status(_events["error"])
    assert _obj.events[-1][1:] == _events["error"], "Last event should be error"

    # Act & Assert for "critical" event
    _obj.set_event_status(_events["critical"])
    assert _obj.events[-1][1:] == _events["critical"], "Last event should be critical"


def test_003_C_Inspector_M_look_up(
    diagnosing: Tuple[Dict[str, Tuple[int, int, int, str]], Mock]
) -> None:
    """
    Test function for diagnosing events.

    This function tests the event handling of an object. It sets the event status for each event in the dictionary
    and asserts the return value of the `look_up` method based on the event key.

    Args:
        diagnosing (Tuple[Any, Dict[str, Any]]): A tuple containing an object and a dictionary of events.

    Raises:
        AssertionError: If the `look_up` method does not return the expected boolean value.
    """
    _obj = Inspector(
        logger_name="test_003_C_Inspector_M_look_up",
        logger_level=logging.INFO,
        stream_handler_enable=True,
        file_handler_enable=True,
        dtc_level=logging.WARNING,
    )
    _events, _ = diagnosing

    for key, value in _events.items():
        _obj.set_event_status(value)
        if key in ["debug", "info"]:
            assert not _obj.look_up(
                value
            ), f"Expected False for key {key}, but got True"
        else:
            assert _obj.look_up(value), f"Expected True for key {key}, but got False"


def test_004_C_Inspector_M_clean_up(
    diagnosing: Tuple[Dict[str, Tuple[int, int, int, str]], Mock]
) -> None:
    """
    Test function for a diagnosing object.

    This function tests the methods `set_event_status`, `look_up`, and `clean_up`
    of a diagnosing object.

    Args:
        diagnosing (Tuple[Any, Dict[str, Any]]): A tuple containing a diagnosing object
        and a dictionary of events.

    Raises:
        AssertionError: If the `look_up` or `clean_up` methods of the diagnosing object
        do not behave as expected.
    """
    _obj = Inspector(
        logger_name="test_004_C_Inspector_M_clean_up",
        logger_level=logging.INFO,
        stream_handler_enable=True,
        file_handler_enable=True,
        dtc_level=logging.WARNING,
    )
    _events, _ = diagnosing

    for key, value in _events.items():
        _obj.set_event_status(value)

    for key, value in _events.items():
        if key in ["debug", "info"]:
            assert not _obj.clean_up(value), f"Event {value} should not exist."
        else:
            assert _obj.clean_up(value), f"Event {value} could not be cleaned up."
            assert not _obj.look_up(
                value
            ), f"Event {value} should not exist after cleanup."


def test_005_C_Inspector_M_clear_DTC(
    diagnosing: Tuple[Dict[str, Tuple[int, int, int, str]], Mock]
) -> None:
    """
    Test function for a diagnosing object.

    This function tests the methods `set_event_status`, `clear_DTC`
    of a diagnosing object.

    Args:
        diagnosing (Tuple[Any, Dict[str, Any]]): A tuple containing a diagnosing object
        and a dictionary of events.

    Raises:
        AssertionError: If the `events` attribute of the diagnosing object
        is not empty after calling `clear_DTC`.
    """
    _obj = Inspector(
        logger_name="test_005_C_Inspector_M_clear_DTC",
        logger_level=logging.INFO,
        stream_handler_enable=True,
        file_handler_enable=True,
    )
    _events, _ = diagnosing

    _obj.set_event_status(_events["critical"])
    _obj.clear_DTC()
    assert not _obj.events, "Events should be empty after clear_DTC."


@patch("builtins.open", new_callable=mock_open)
def test_006_C_Inspector_M_dump_DTC(
    mock_file, diagnosing: Tuple[Dict[str, Tuple[int, int, int, str]], Mock]
) -> None:
    """
    Test case for the `dump_DTC` method of a `diagnostic_obj` object.

    Args:
        mock_file (Mock): A mock object for the built-in `open` function.
        monkeypatch (Any): A pytest fixture for safely setting/deleting an attribute/item.
        diagnosing (Tuple[Inspector, Dict[str, Tuple[int, int, int, str]], Mock]): A tuple containing a diagnostic object and events.

    Returns:
        None
    """
    _obj = Inspector(
        logger_name="test_006_C_Inspector_M_dump_DTC",
        logger_level=logging.INFO,
        stream_handler_enable=True,
        file_handler_enable=True,
    )
    _events, _ = diagnosing
    mock_file.reset_mock()

    _obj.dump_DTC()
    mock_file().assert_not_called()
    mock_file.reset_mock()

    _obj.set_event_status(_events["critical"])
    _obj.dump_DTC()

    mock_file.assert_called_once_with("./log/DTC.log", "a")
    mock_file().write.assert_called_once()


def test_007_C_Inspector_P_last_event(
    diagnosing: Tuple[Dict[str, Tuple[int, int, int, str]], Mock]
):
    """
    Test function for the 'last_event' property of the 'Inspector' class.

    This function tests whether the 'last_event' property of an 'Inspector'
    instance correctly returns the last event with its timestamp.

    Parameters:
    diagnosing (tuple): A tuple containing an instance of 'Inspector' and a dictionary of events.
    monkeypatch (object): A monkeypatch object for mocking.

    Returns:
    None
    """

    _obj = Inspector(
        logger_name="test_007_C_Inspector_P_last_event",
        logger_level=logging.INFO,
        stream_handler_enable=True,
        file_handler_enable=True,
    )
    _events, _ = diagnosing

    # Set the event status to "error"
    _obj.set_event_status(_events["error"])

    # Assert that the 'last_event' property returns the correct value
    assert (str(datetime.now()), *_events["error"]) == _obj.last_event


def test_008_C_Inspector_B_logging_handling_disable() -> None:
    """
    Test the logging handling function.

    Args:
        monkeypatch (object): The monkeypatch fixture from pytest.
        diagnosing (Tuple[object, Dict[str, str]]): A tuple containing a test object and a dictionary of events.

    Returns:
        None
    """

    # Arrange
    _obj = Inspector(
        logger_name="test_008_C_Inspector_B_logging_handling_disable",
        stream_handler_enable=False,
        file_handler_enable=False,
    )

    file_handlers = [
        h for h in _obj.logger.handlers if isinstance(h, logging.FileHandler)
    ]
    stream_handlers = [
        h for h in _obj.logger.handlers if isinstance(h, logging.StreamHandler)
    ]

    # Act

    # Assert
    assert logging.DEBUG == _obj.logger.level
    assert 0 == len(file_handlers)
    assert 0 == len(stream_handlers)


@patch("builtins.open", new_callable=mock_open)
def test_009_C_Inspector_M_dump_DTC_disable(
    mock_file, diagnosing: Tuple[Dict[str, Tuple[int, int, int, str]], Mock]
) -> None:
    """
    Test case for the `dump_DTC` method of a `diagnostic_obj` object.

    Args:
        mock_file (Mock): A mock object for the built-in `open` function.
        monkeypatch (Any): A pytest fixture for safely setting/deleting an attribute/item.
        diagnosing (Tuple[Inspector, Dict[str, Tuple[int, int, int, str]], Mock]): A tuple containing a diagnostic object and events.

    Returns:
        None
    """
    _obj = Inspector(
        logger_name="test_009_C_Inspector_M_dump_DTC_disable",
        logger_level=logging.INFO,
        stream_handler_enable=True,
        file_handler_enable=True,
        dtc_table_enable=False,
    )
    _events, _ = diagnosing
    mock_file.reset_mock()

    _obj.set_event_status(_events["critical"])
    _obj.dump_DTC()

    mock_file.assert_not_called()


def test_010_C_Inspector_B_dupplicated_calls() -> None:
    """
    Test the logging handling function.

    Args:
        monkeypatch (object): The monkeypatch fixture from pytest.
        diagnosing (Tuple[object, Dict[str, str]]): A tuple containing a test object and a dictionary of events.

    Returns:
        None
    """

    # Arrange
    Inspector(
        logger_name="test_010_C_Inspector_B_raise_exception",
    )

    Inspector(
        logger_name="test_010_C_Inspector_B_raise_exception",
    )

    count = sum(
        1
        for instance in Inspector._instances
        if instance.name == "test_010_C_Inspector_B_raise_exception"
    )

    assert 1 == count


################################################################################
#                                END OF FILE                                   #
################################################################################
