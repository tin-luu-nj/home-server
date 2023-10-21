import logging
from datetime import datetime
from typing import List, Tuple, Union

from ._CONST_ import *


class clsDiagnostic:
    """
    A class used for logging purposes.

    Attributes
    ----------
    events : list
        A list to store events.
    logger : logging.Logger
        A logger to handle logging.

    Methods
    -------
    __init__()
        Initializes the Diagnostic class and sets up logging handlers.
    """

    def __init__(self) -> None:
        """
        Initializes the Diagnostic class and sets up logging handlers.
        """

        self.events: List = []
        self.logger: logging.Logger = logging.getLogger(__name__)

        if LOGGING_HANDLER_FILE_ENABLE or LOGGING_HANDLER_STREAM_ENABLE:
            self._setup_logging_handlers()

    def _setup_logging_handlers(self) -> None:
        """
        Sets up the logging handlers.
        """

        if LOGGING_HANDLER_FILE_ENABLE:
            self._setup_stream_handler()

        if LOGGING_HANDLER_STREAM_ENABLE:
            self._setup_file_handler()

        self.logger.setLevel(logging.DEBUG)

    def _setup_stream_handler(self) -> None:
        """
        Sets up the stream handler for logging.
        """

        stream_handler = logging.StreamHandler()
        stream_format = logging.Formatter(
            "%(relativeCreated)s\t%(levelname)s\t%(message)s"
        )
        stream_handler.setFormatter(stream_format)
        self.logger.addHandler(stream_handler)

    def _setup_file_handler(self) -> None:
        """
        Sets up the file handler for logging.
        """

        file_handler = logging.FileHandler(FILE_LOG)
        file_format = logging.Formatter("%(asctime)s\t%(levelname)s\t\t%(message)s")
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)

    def clear_DTC(self) -> None:
        """Clears the events list."""
        self.events.clear()

    def clean_up(self, event: Tuple[int, int, int, str]) -> bool:
        """
        Removes an event from the events list.

        Parameters:
        event (Tuple[int, int, int, str]): The event to remove.

        Returns:
        bool: True if the event was found and removed, False otherwise.
        """
        for id, entry in enumerate(self.events):
            if event[:3] == entry[1:4]:
                del self.events[id]
                return True
        return False

    def set_event_status(self, event: Tuple[int, int, int, str]) -> None:
        """
        Logs the event and adds it to the events list if its logging level is high enough.

        Parameters:
        event (Tuple[int, int, int, str]): The event to set the status for.
        """
        self._logging(event[0])(event[3])

        if event[0] >= DTC_LEVEL:
            self.events.append((str(datetime.now()), *event))

    def _logging(self, log_level: int) -> callable:
        """
        Returns the appropriate logging function for the given log level.

        Parameters:
        log_level (int): The log level.

        Returns:
        callable: The logging function.
        """
        return [
            self.logger.critical,
            self.logger.error,
            self.logger.warning,
            self.logger.info,
            self.logger.debug,
        ][LOGGING_LEVEL_LIST.index(log_level)]

    def look_up(self, event: Tuple[int, int, int, str]) -> bool:
        """
        Checks if an event is in the events list.

        Parameters:
        event (Tuple[int, int, int, str]): The event to look up.

        Returns:
        bool: True if the event is in the events list, False otherwise.
        """
        return any(event[:3] == entry[1:4] for entry in self.events)

    def dump_DTC(self) -> None:
        """Writes the events list to a file."""
        if DTC_LOG:
            with open(FILE_DTC, OPEN_PERMISSION_APPEND) as stream:
                for entry in self.events:
                    stream.write(f"{entry}\n")

    @property
    def last_event(self) -> Union[Tuple[str, int, int, int], Tuple]:
        """
        Returns the last event in the events list.

        Returns:
        Union[Tuple[str, int, int, int], Tuple]: The last event or an empty tuple if there are no events.
        """
        return self.events[-1] if self.events else ()
