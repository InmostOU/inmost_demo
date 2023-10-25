import logging
from typing import Union


class CustomLogger(logging.Logger):
    def __init__(self, logger_name: str, log_level: Union[int, str] = logging.INFO):
        super(CustomLogger, self).__init__(logger_name, log_level)
        self.handlers.clear()

        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(stream_formatter)
        self.addHandler(stream_handler)


Logger = CustomLogger("lambda-lib_logger", logging.DEBUG)
