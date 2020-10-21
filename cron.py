import configparser
import time
import os

from datetime import datetime
from crontab import CronTab

import const
from logger import setup_logger

NEXT_ENTRIES = 10


def create_config(path):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "crontab", "")

    with open(path, "w") as config_file:
        config.write(config_file)


def get_next_entries(job, next_entries_num):
    schedule = job.schedule(date_from=datetime.now())
    next_entries = []
    for entry in range(next_entries_num):
        next_entries.append(str(schedule.get_next(datetime)))
    return next_entries


def run_cron(cron):
    logger.info("Cron started")
    for result in cron.run_scheduler(cadence=5, warp=True):
        logger.info(result)


def read_config_for_crontab_path(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    if os.path.isfile(config_path):
        try:
            crontab_path = config.get("Settings", "crontab")
            logger.info("crontab path {0}".format(crontab_path))
            return crontab_path
        except configparser.NoSectionError as e:
            logger.error(str(e) + ". Please specify section [Settings]")
        except configparser.NoOptionError as e:
            logger.error(str(e) + ". Please specify path for crontab as \ncrontab=/path/to/crontab")
    else:
        print("No config fount at {0}".format(const.ABS_PATH))
        create_config(config_path)
        time.sleep(1)
        print("Config created at {0} \nPlease specify crontab path.".format(config_path))
        logger.warning("No config found. Config created at {0}".format(config_path))


def init_cron(crontab_path):
    if not crontab_path:
        logger.warning("Crontab path in config is empty")
    else:
        try:
            cron = CronTab(tabfile=crontab_path, user="andrew")
        except FileNotFoundError as e:
            logger.error(e)
        except IsADirectoryError as e:
            logger.error(e)
        else:
            logger.info("Reading crontab at {0}".format(crontab_path))
            if cron.__len__() > 0:
                for job in range(cron.__len__()):
                    logger.info("Found job {0}:".format(job) + "\t" + str(cron[job]))
                    logger.info("Next {0} entries:".format(NEXT_ENTRIES))
                    for entry in range(get_next_entries(cron[job], NEXT_ENTRIES).__len__()):
                        logger.info("{0}\t".format(entry + 1) + get_next_entries(cron[job], NEXT_ENTRIES)[entry])
                try:
                    run_cron(cron)
                except KeyboardInterrupt as e:
                    logger.info("Cron finished {0}".format(e))
            else:
                logger.warning("No cron jobs found at {0}".format(crontab_path))

                
if __name__ == "__main__":
    logger = setup_logger(const.LOG_PATH)
    logger.info("Cron started")
    init_cron(read_config_for_crontab_path(const.CONFIG_PATH))
