from datetime import datetime
import logging

from config.cfg import DIAGNOSTIC
from src.pyDiagnostic.__literals__ import *


class clsDiagnostic(object):
    def __init__(self) -> None:
        self.events = list()
        if (
            DIAGNOSTIC.LOGGING_HANDLER_FILE_ENABLE
            or DIAGNOSTIC.LOGGING_HANDLER_STREAM_ENABLE
        ):
            self.logger = logging.getLogger(__name__)

        if DIAGNOSTIC.LOGGING_HANDLER_FILE_ENABLE:
            # Create handlers
            c_handler = logging.StreamHandler()
            # Create formatters and add it to handlers
            c_format = logging.Formatter(
                "%(relativeCreated)s\t%(levelname)s\t%(message)s"
            )
            c_handler.setFormatter(c_format)
            self.logger.addHandler(c_handler)

        if DIAGNOSTIC.LOGGING_HANDLER_STREAM_ENABLE:
            # Create handlers
            f_handler = logging.FileHandler(FILE_LOG)
            # Create formatters and add it to handlers
            f_format = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
            f_handler.setFormatter(f_format)
            self.logger.addHandler(f_handler)

        if (
            DIAGNOSTIC.LOGGING_HANDLER_FILE_ENABLE
            or DIAGNOSTIC.LOGGING_HANDLER_STREAM_ENABLE
        ):
            # TODO
            self.logger.setLevel(logging.DEBUG)

    def clear_DTC(self) -> None:
        self.events.clear()

    def clean_up(self, event: tuple[int, int, int, str]):
        found = -1
        for id, entry in enumerate(self.events):
            if (
                event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX],
                event[DEM_EVENT_TUPLE_ID_INDEX],
                event[DEM_EVENT_TUPLE_STATUS_INDEX],
            ) == entry[1:]:
                found = id
                break
        if not found == -1:
            del self.events[found]
            return True
        return False

    def set_event_status(self, event: tuple[int, int, int, str]):
        self._logging(event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX])(
            event[DEM_EVENT_TUPLE_NAME_INDEX]
        )

        if (
            event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX]
            >= LOGGING_LEVEL_LIST[LOG_LEVEL_KEYWORD.index(DIAGNOSTIC.DTC_LEVEL)]
        ):
            self.events.append(
                (
                    str(datetime.now()),
                    event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX],
                    event[DEM_EVENT_TUPLE_ID_INDEX],
                    event[DEM_EVENT_TUPLE_STATUS_INDEX],
                )
            )

    def _logging(self, log_level):
        logging_function = [
            self.logger.critical,
            self.logger.error,
            self.logger.warning,
            self.logger.info,
            self.logger.debug,
        ]

        return logging_function[LOGGING_LEVEL_LIST.index(log_level)]

    def look_up(self, event: tuple[int, int, int, str]):
        for entry in self.events:
            if (
                event[DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX],
                event[DEM_EVENT_TUPLE_ID_INDEX],
                event[DEM_EVENT_TUPLE_STATUS_INDEX],
            ) == entry[1:]:
                return True
        return False

    def dump_DTC(self):
        if DIAGNOSTIC.DTC_LOG:
            with open(FILE_DTC, OPEN_PERMISSION_APPEND) as stream:
                for entry in self.events:
                    stream.write(f"{entry}\n")

    @property
    def last_event(self):
        if len(self.events) > LEN_ZERO:
            return self.events[LIST_ELEMENT_INDEX_LAST]
        else:
            return ()
