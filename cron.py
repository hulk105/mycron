import configparser
import time
import os
from datetime import datetime

from crontab import CronTab

from logger import logger


ABS_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = ABS_PATH + "/config.conf"
CRONTAB_PATH = ABS_PATH + "/crontab"


def create_config(path):
    """
    Create config file
    """
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


if __name__ == "__main__":
    while True:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        if os.path.isfile(CONFIG_PATH):
            try:
                crontab_path = config.get("Settings", "crontab")
            except configparser.NoSectionError as e:
                logger.error(str(e) + ". Please specify section [Settings]")
                break
            except configparser.NoOptionError as e:
                logger.error(str(e) + ". Please specify path for crontab as \ncrontab=/pat/to/crontab")
                break
            else:
                """
                Crontab
                """
                if not crontab_path:
                    logger.warning("Crontab path is empty")
                else:
                    cron = CronTab(tabfile=crontab_path, user="andrew")

                    """
                    Jobs
                    """
                    if cron.__len__() > 0:
                        logger.info("Crontab jobs at {0}:".format(crontab_path))
                        for job in range(cron.__len__()):
                            logger.info("Job {0}:".format(job) + " " + str(cron[job]))

                            # Next entries
                            logger.info("Next entries:")
                            for entry in get_next_entries(cron[job], 10):
                                logger.info(entry)
                        try:
                            run_cron(cron)
                        except KeyboardInterrupt as e:
                            logger.info("Cron finished. {0}".format(e))
                    else:
                        logger.info("Crontab is empty")
                break
        else:
            print("No config fount at {0}".format(ABS_PATH))
            create_config(CONFIG_PATH)
            time.sleep(1)
            print("Config created at {0} \nPlease specify crontab path.".format(CONFIG_PATH))
            logger.warning("No config found. Config created at {0}".format(CONFIG_PATH))

        time.sleep(1)
