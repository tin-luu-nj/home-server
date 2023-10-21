from typing import List

# File open modes
OPEN_PERMISSION_READ: str = "r"
OPEN_PERMISSION_WRITE: str = "w"
OPEN_PERMISSION_APPEND: str = "a"

# Index of the last element in a list
LIST_ELEMENT_INDEX_LAST: int = -1

# Length of an empty list or string
LEN_ZERO: int = 0

# Indices of the elements in an event tuple
DEM_EVENT_TUPLE_LOGGING_LEVEL_INDEX: int = 0
DEM_EVENT_TUPLE_ID_INDEX: int = 1
DEM_EVENT_TUPLE_STATUS_INDEX: int = 2
DEM_EVENT_TUPLE_NAME_INDEX: int = 3

# Flags to enable or disable logging handlers
LOGGING_HANDLER_FILE_ENABLE: bool = True
LOGGING_HANDLER_STREAM_ENABLE: bool = True

# Path to the log file
FILE_LOG: str = "log/DDX.log"

# Logging Levels
LOGGING_LEVEL_CRITICAL: int = 50
LOGGING_LEVEL_ERROR: int = 40
LOGGING_LEVEL_WARNING: int = 30
LOGGING_LEVEL_INFO: int = 20
LOGGING_LEVEL_DEBUG: int = 10

# List of logging levels
LOGGING_LEVEL_LIST: List[int] = [
    LOGGING_LEVEL_CRITICAL,
    LOGGING_LEVEL_ERROR,
    LOGGING_LEVEL_WARNING,
    LOGGING_LEVEL_INFO,
    LOGGING_LEVEL_DEBUG,
]

# Keywords corresponding to logging levels
LOG_LEVEL_KEYWORD: List[str] = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

# DTC level and log flag
DTC_LEVEL: int = 30
DTC_LOG: bool = True

# Path to the DTC log file
FILE_DTC: str = "./log/DTC.log"
