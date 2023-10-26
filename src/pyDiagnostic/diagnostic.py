import logging
import sys
from datetime import datetime
from typing import List, Tuple, Union

from ._CONST_ import *


class Inspector:
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
        Initializes the Inspector class and sets up logging handlers.
    """
    _instances = []
    def __new__(cls, *args, **kwargs):
        if cls._instances:
            for instance in cls._instances:
                if kwargs['logger_name'] == instance.name:
                    return instance

        cls._instances.append(super(Inspector, cls).__new__(cls))
        return cls._instances[-1]

    def __init__(
        self,
        logger_name: str = "Wayne",
        logger_level: int = logging.DEBUG,
        stream_handler_enable: bool = True,
        file_handler_enable: bool = True,
        file_handler_path: str = "log/DDX.log",
        dtc_table_enable: bool = True,
        dtc_level: int = logging.INFO,
        dtc_file_path: str = "./log/DTC.log",
    ) -> None:
        """
        Initializes the Inspector class and sets up logging handlers.
        """

        self.name = logger_name
        self.events: List = []
        self.logger: logging.Logger = logging.getLogger(logger_name)

        self.file_handler_path = file_handler_path
        self.dtc = dtc_table_enable
        self.dtc_level = dtc_level
        self.dtc_file_path = dtc_file_path

        if stream_handler_enable:
            self._setup_stream_handler()

        if file_handler_enable:
            self._setup_file_handler()

        self.logger.setLevel(logger_level)

    def _setup_stream_handler(self) -> None:
        """
        Sets up the stream handler for logging.
        """

        _handler = logging.StreamHandler(sys.stdout)
        _format = logging.Formatter("%(relativeCreated)s\t%(levelname)s\t%(message)s")
        _handler.setFormatter(_format)
        _handler.setLevel(logging.DEBUG)
        self.logger.addHandler(_handler)

    def _setup_file_handler(self) -> None:
        """
        Sets up the file handler for logging.
        """

        _handler = logging.FileHandler(self.file_handler_path)
        _format = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
        _handler.setFormatter(_format)
        _handler.setLevel(logging.DEBUG)
        self.logger.addHandler(_handler)

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
        if event[0] >= self.logger.level:
            log_level_dict = {
                logging.CRITICAL: self.logger.critical,
                logging.ERROR: self.logger.error,
                logging.WARNING: self.logger.warning,
                logging.INFO: self.logger.info,
                logging.DEBUG: self.logger.debug,
            }

            log_level_dict[event[0]](event[3])

        if event[0] >= self.dtc_level:
            self.events.append((str(datetime.now()), *event))

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
        if self.dtc:
            with open(self.dtc_file_path, OPEN_PERMISSION_APPEND) as stream:
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


################################################################################
#                                END OF FILE                                   #
################################################################################
