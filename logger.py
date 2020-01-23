"""
Logger
"""
import logging
import os
import time

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = ABS_PATH + "/mycron.log"


if not os.path.isfile(LOG_PATH):
    with open(LOG_PATH, "w") as log_file:
        print("Log created at {0}".format(LOG_PATH))
        time.sleep(1)
else:
    pass
logger = logging.getLogger("mycron")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_PATH)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
