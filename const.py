from os.path import dirname, join


ABS_PATH = dirname(__file__)
CONFIG_PATH = join(ABS_PATH, 'config.conf')
CRONTAB_PATH = join(ABS_PATH, 'crontab')
LOG_PATH = join(ABS_PATH, 'mycron.log')

print(ABS_PATH)