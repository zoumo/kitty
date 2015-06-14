#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
based on logging
This utils is independent, you can use it with out anyother module

[usage]
import kitty.utils.log
kitty.utils.log.getLogger(name)

notice:
if use name like kitty.test, the log will output to it's father kitty[default console]

"""

import os
import sys
import time
import logging
import logging.config
import logging.handlers

try:
    import thread
    import threading
except ImportError:
    thread = None

# ----------------------------------------------------------------------------
#   personal info
# ----------------------------------------------------------------------------

__author__  = "Jim Zhang"
__version__ = "0.1.1.0"
__date__    = "18/09/2014"

# ----------------------------------------------------------------------------
#   Miscellaneous module data
# ----------------------------------------------------------------------------

NONE    = 0x00 #0000 0000
DEBUG   = 0x01 #0000 0001
TRACE   = 0x02 #0000 0010
NOTICE  = 0x04 #0000 0100
WARNING = 0x08 #0000 1000
FATAL   = 0x10 #0001 0000
ALL     = 0xFF #1111 1111

_LEVEL_NAME_MAP = {
    NONE      : 'NONE',
    DEBUG     : 'DEBUG',
    TRACE     : 'TRACE',
    NOTICE    : 'NOTICE',
    WARNING   : 'WARNING',
    FATAL     : 'FATAL',
}

_NAME_LEVEL_MAP = {
    'NONE'    : NONE,
    'DEBUG'   : DEBUG,
    'TRACE'   : TRACE,
    'NOTICE'  : NOTICE,
    'WARNING' : WARNING,
    'FATAL'   : FATAL,
}

for level in _LEVEL_NAME_MAP:
    logging.addLevelName(level, _LEVEL_NAME_MAP[level])

ROOT_LOGGER_NAME = 'kitty'

# ---------------------------------------------------------------------
#   thread safe
# ---------------------------------------------------------------------

if thread:
    _lock = threading.RLock()
else:
    _lock = None
def _acquireLock():
    """
    Acquire the module-level lock for serializing access to shared data.

    This should be released with _releaseLock().
    """
    if _lock:
        _lock.acquire()

def _releaseLock():
    """
    Release the module-level lock acquired by calling _acquireLock().
    """
    if _lock:
        _lock.release()

# -----------------------------------------------------------------------------
#   new filter class
# -----------------------------------------------------------------------------
class SysFilter(logging.Filter):
    def __init__(self, level, name=''):
        # be careful for super()
        super(SysFilter, self).__init__(name)
        self.logLevel = level

    def filter(self, record):
        if record.levelno & self.logLevel :
            return True
        return False
# -----------------------------------------------------------------------------
#   new Logger class
# -----------------------------------------------------------------------------
class SysLogger(logging.Logger):

    def debug(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        apply(self._log, (DEBUG, msg, args), kwargs)

    def notice(self, msg, *args, **kwargs):

        apply(self._log, (NOTICE, msg, args), kwargs)

    def trace(self, msg, *args, **kwargs):
        apply(self._log, (TRACE, msg, args), kwargs)

    def warning(self, msg, *args, **kwargs):
        apply(self._log, (WARNING, msg, args), kwargs)

    def fatal(self, msg, *args, **kwargs):
        apply(self._log, (FATAL, msg, args), kwargs)
# -----------------------------------------------------------------------------
#   default conf
# -----------------------------------------------------------------------------

# DEFAULT_LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters' : {
#         'default_formatter' : {
#             'format'  : DEFAULT_LOG_FORMAT,
#             'datefmt' : DEFAULT_TIME_FORMAT,
#         },
#     },
#     'filters': {
#         'default_filter': {
#             '()'    : SysFilter, # callable
#             'name'  : 'default_filter',
#             'level' : DEFAULT_LOG_LEVEL,
#         },
#     },
#     'handlers': {
#         'console': {
#             'level'     : 'DEBUG',
#             'class'     : 'logging.StreamHandler',
#             'formatter' : 'default_formatter',
#         },
#     },
#     'loggers': {
#         'kitty': {
#             'handlers': ['console'],
#             'filters' : ['default_filter'],
#         },
#     }
# }

DEFAULT_LOG_FORMAT  = ("%(levelname)s: [%(asctime)s] [%(name)s] [%(thread)d]"
                       " [%(filename)s:%(lineno)d:%(funcName)s] %(message)s")
DEFAULT_TIME_FORMAT = "%y-%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL   = ALL # NOTICE | WARNING | FATAL

default_formatter   = logging.Formatter(DEFAULT_LOG_FORMAT, DEFAULT_TIME_FORMAT)
default_filter      = SysFilter(DEFAULT_LOG_LEVEL, 'default_filter')

# set a new logger class
logging.setLoggerClass(SysLogger)

# # default logger
# root = logging.getLogger('kitty')

# # Avoid follows
# # setLevel(NONE) or do nothing will lead to loop through this logger and
# # its parents in the logger hierarchy, looking for a non-zero logging level
# root.setLevel(DEBUG)

# root.addFilter(default_filter)
# hdlr = logging.StreamHandler()
# hdlr.setFormatter(default_formatter)
# root.addHandler(hdlr)

_loggers = {}

# -----------------------------------------------------------------------------
#   class level function
# -----------------------------------------------------------------------------

def getLogger(name=ROOT_LOGGER_NAME, **kwargs):
    """
    args:
    name        logger name
    level       available log level like (DEBUG | NOTICE | FATAL)
                default ALL
    filename    ./log/test.log
    format      log string format
    datefmt     date string format
    """

    if name in _loggers:
        return _loggers[name]

    _acquireLock()
    try:
        logger = logging.getLogger(name)

        # filter
        level = kwargs.get("level", DEFAULT_LOG_LEVEL)
        if level == DEFAULT_LOG_LEVEL:
            filt = default_filter
        else:
            filt = SysFilter(level)

        logger.addFilter(filt)

        # formatter
        fmt = kwargs.get("format", DEFAULT_LOG_FORMAT)
        datefmt = kwargs.get("datefmt", DEFAULT_TIME_FORMAT)

        if fmt == DEFAULT_LOG_FORMAT and datefmt == DEFAULT_TIME_FORMAT:
            formatter = default_formatter
        else:
            formatter = logging.Formatter(fmt, datefmt)

        # Avoid follows
        # setLevel(NONE) or do nothing will lead to loop through this logger and
        # its parents in the logger hierarchy, looking for a non-zero logging level
        logger.setLevel(DEBUG)

        # handlers
        # no need to call hdlr.createLock(), it is called in hdlr.__init__()
        filename = kwargs.get("filename")
        if filename:
            hdlr = logging.handlers.TimedRotatingFileHandler(filename, when='d')
        else:
            hdlr = logging.StreamHandler()

        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

        _loggers[name] = logger

    finally:
        _releaseLock()

    return logger

root = getLogger()

# -----------------------------------------------------------------------------
#    test
# -----------------------------------------------------------------------------
def test():

    # all function test
    logger = getLogger()
    logger.debug("this is debug")
    logger.notice("this is notice")
    logger.trace("this is trace")
    logger.warning("this is warning")
    logger.fatal("this is fatal")



    LOG_CONFIG = {
        'file': {
            'name' : 'file',
            'filename' : './file.log',
            'level' : NOTICE | WARNING | FATAL,
        },
        'other': {
            'name' : 'other',
            'level': DEBUG | WARNING,
        },
        'kitty.other': {
            'name' : 'kitty.other',
            'level': NOTICE | DEBUG,
        },
    }

    # namespace test
    logger = getLogger(**LOG_CONFIG['other'])
    logger.debug("this is debug")
    logger.warning("this is warning")

    # this will print twice
    logger = getLogger(**LOG_CONFIG['kitty.other'])
    logger.debug("this is debug")
    logger.fatal("this is fatal")

    file_logger = getLogger(**LOG_CONFIG['file'])
    file_logger.debug("this is debug")
    file_logger.notice("this is notice")
    file_logger.trace("this is trace")
    file_logger.warning("this is warning")
    file_logger.fatal("this is fatal")




if __name__ == '__main__':
    test()
