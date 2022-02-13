import logging
from logging import StreamHandler
import re


def init_base_logger():
    my_logger = logging.getLogger("my_logger")
    my_logger.setLevel(logging.INFO)
    my_logger.propagate = 0

    handler = StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s/%(funcName)s] : %(message)s')
    handler.setFormatter(formatter)
    handler.suffix = "%Y%m%d"
    handler.extMatch = re.compile(r"^\d{8}$")

    my_logger.addHandler(handler)
    return my_logger


