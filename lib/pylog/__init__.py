#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
To use, simply 'import pylog' and pylog.init(filename)
based on logging
"""

import os, sys, time, logging, logging.handlers

__all__ = ['NONE', 'DEBUG', 'TRACE', 'NOTICE', 'WARNING', 'FATAL', 'ALL',
           'DEFAULT_LOG_FORMAT', 'DEFAULT_TIME_FORMAT', 'DEFAULT_LOG_LEVEL'
           'init', 'pylogger']


__author__  = "Jim Zhang"
__status__  = "production"
# Note: the attributes below are no longer maintained.
__version__ = "0.1.0.0"
__date__    = "24/08/2014"

#---------------------------------------------------------------------------
#   Miscellaneous module data
#---------------------------------------------------------------------------

NONE    = 0x00; #0000 0000
DEBUG   = 0x01; #0000 0001
TRACE   = 0x02; #0000 0010
NOTICE  = 0x04; #0000 0100
WARNING = 0x08; #0000 1000
FATAL   = 0x10; #0001 0000
ALL     = 0xFF; #1111 1111

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

#------------------------------------------------------------------------------
#   default conf
#------------------------------------------------------------------------------

DEFAULT_LOG_FORMAT  = "%(levelname)-9s: %(asctime)s : [%(thread)d] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s"
DEFAULT_TIME_FORMAT = "%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL = ALL #NOTICE | WARNING | FATAL

_HAS_INIT = False
pylogger = None

#------------------------------------------------------------------------------
#   init function
#------------------------------------------------------------------------------
def init(filename, loglvl = DEFAULT_LOG_LEVEL, fmt = DEFAULT_LOG_FORMAT, datefmt = DEFAULT_TIME_FORMAT):
    """
    args:
    filename
    loglvl    available log level   default ALL
    fmt       log format string     default %(levelname)-9s: %(asctime)s : [%(thread)d] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s
    datefmt   date format string    default %m-%d %H:%M:%S
    """
    global _HAS_INIT
    global pylogger

    if _HAS_INIT:
        print "pylogger has inited"
        return

    for level in _LEVEL_NAME_MAP:
        logging.addLevelName(level, _LEVEL_NAME_MAP[level])
    # user-definded log class
    logging.setLoggerClass(SysLog)
    pylogger = logging.getLogger('syslog')

    hdlr = logging.handlers.TimedRotatingFileHandler(filename, when='d')
    fmtr = logging.Formatter(fmt, datefmt)

    hdlr.setFormatter(fmtr)
    pylogger.addHandler(hdlr)
    # need this statement
    pylogger.setLevel(NONE)

    filt = SysLogFilter(loglvl)
    pylogger.addFilter(filt)

    _HAS_INIT = True


#------------------------------------------------------------------------------
#   SysLog filter
#------------------------------------------------------------------------------
class SysLogFilter(logging.Filter):
    def __init__(self, level, name=''):
        logging.Filter.__init__(self, name)
        self.logLevel = level

    def filter(self, record):
        if record.levelno & self.logLevel :
            return True
        return False
#------------------------------------------------------------------------------
#   SysLog class
#------------------------------------------------------------------------------
class SysLog(logging.Logger):


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
        apply(self._log, (WARNING, msg, args), kwargs)

# -----------------------------------------------------------------------------
#    test
# -----------------------------------------------------------------------------
def test():
    init('test.log')

    pylogger.debug("this is debug")
    pylogger.notice("this is notice")
    pylogger.trace("this is trace")
    pylogger.warning("this is warning")
    pylogger.fatal("this is fatal")

if __name__ == '__main__':
    test()
