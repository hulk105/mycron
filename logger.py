"""
Logger
"""
import logging
import os
import time

from const import LOG_PATH


def setup_logger(log_path):
    if not os.path.isfile(log_path):
        with open(log_path, "w") as log_file:
            print("Log created at {0}".format(log_path))
            time.sleep(1)
    else:
        pass
    logger = logging.getLogger("mycron")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
