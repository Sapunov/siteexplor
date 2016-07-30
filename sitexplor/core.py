"""
ADUKE core
"""

import logging
import logging.handlers

from sitexplor import settings


def set_logger(level=logging.DEBUG, log_namespace=settings.PROGRAM_NAMESPACE):

    log_file = settings.LOGFILE
    log_format = settings.LOG_FORMAT

    date_format = settings.LOG_TIMEFORMAT

    log = logging.getLogger(log_namespace)
    log.setLevel(level)

    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=20 * 1024 ** 2,
        backupCount=5)

    handler.setFormatter(logging.Formatter(log_format, date_format))
    log.addHandler(handler)
