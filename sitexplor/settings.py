"""
Sitexplor settings
"""

import os

PROGRAM_NAMESPACE = "sitexplor"

LOG_TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "%(asctime)s.%(msecs)03d | %(levelname)s: %(filename)s:%(lineno)d: %(message)s"

PROGRAM_PATH = "/opt/sitexplor"
DATADIR = os.path.join(PROGRAM_PATH, "data")
SITES_DIR = os.path.join(DATADIR, "sites")
URLS_FILE = os.path.join(DATADIR, "urls_database")

LOGFILE = os.path.join(DATADIR, "logs/{0}.log".format(PROGRAM_NAMESPACE))

DEBUG = False
