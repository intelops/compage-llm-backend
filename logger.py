import logging
import sys


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "WARNING": "\033[93m",  # yellow
        "ERROR": "\033[91m",  # red
        "CRITICAL": "\033[91m",  # red
        "INFO": "\033[92m",  # green
    }
    RESET_COLOR = "\033[0m"

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            levelname_color = f"{self.COLORS[levelname]}{levelname}{self.RESET_COLOR}"
            record.levelname = levelname_color
        return super().format(record)


# get logger
logger = logging.getLogger()

# create formatter
formatter = ColoredFormatter("%(levelname)s:\t  %(message)s")

# create handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("log.txt")

# set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handlers to the logger
logger.handlers = [stream_handler, file_handler]

# set log-level
logger.setLevel(logging.INFO)
