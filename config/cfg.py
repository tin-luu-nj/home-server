class cfgDIAGNOSTIC:
    LOGGING_HANDLER_STREAM_ENABLE = True
    LOGGING_HANDLER_STREAM_LEVEL = "DEBUG"
    LOGGING_HANDLER_FILE_ENABLE = True
    LOGGING_HANDLER_FILE_LEVEL = "INFO"
    DTC_ENABLE = True
    DTC_TIMESTAMP = None
    DTC_LEVEL = "WARNING"
    DTC_LOG = True

DIAGNOSTIC = cfgDIAGNOSTIC()