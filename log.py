import logging
import sys
from logging.handlers import RotatingFileHandler
from decouple import config

# FROM:
# https://gist.github.com/nguyenkims/e92df0f8bd49973f0c94bddf36ed7fd0,
# with some modifications

FORMATTER = logging.Formatter(
    "[%(asctime)s] (%(module)s.%(funcName)s) - [%(levelname)s] (%(lineno)d) %(message)s")
LOG_FILE = config('LOG_FILE', default='etl.log')


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = RotatingFileHandler(
        filename=LOG_FILE, maxBytes=16777216, backupCount=5)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(get_file_handler())

    logger.propagate = False

    return logger
