#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This utils is independent, you can use it with out anyother module

To use, simply 'import kitty.utils.log' and kitty.utils.init(filename)
based on logging
"""

import os, sys, time
import logging, logging.handlers

__all__ = ['NONE', 'DEBUG', 'TRACE', 'NOTICE', 'WARNING', 'FATAL', 'ALL',
           'DEFAULT_LOG_FORMAT', 'DEFAULT_TIME_FORMAT', 'DEFAULT_LOG_LEVEL'
           'init', 'logger']


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

for level in _LEVEL_NAME_MAP:
    logging.addLevelName(level, _LEVEL_NAME_MAP[level])

_HAS_INIT = False


#------------------------------------------------------------------------------
#   default conf
#------------------------------------------------------------------------------

DEFAULT_LOG_FORMAT  = "%(levelname)-9s: %(asctime)s : [%(name)s] [%(thread)d] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s"
DEFAULT_TIME_FORMAT = "%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL = ALL # NOTICE | WARNING | FATAL

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'kitty': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}


#------------------------------------------------------------------------------
#   init function
#------------------------------------------------------------------------------
def init(filename, loglvl=DEFAULT_LOG_LEVEL, fmt=DEFAULT_LOG_FORMAT, datefmt=DEFAULT_TIME_FORMAT):
    """
    args:
    filename
    loglvl      available log level
                default ALL
    fmt         log format string
                default %(levelname)-9s: %(asctime)s : [%(name)s] [%(thread)d] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s
    datefmt     date format string
                default %m-%d %H:%M:%S
    """
    global _HAS_INIT
    global logger

    if _HAS_INIT:
        print "logger has inited"
        return



    
    logger = logging.getLogger('kitty.log')

    # Avoid this
    # setLevel(NONE) or do nothing will lead to loop through this logger and
    # its parents in the logger hierarchy, looking for a non-zero logging level
    logger.setLevel(DEBUG)

    filt = SysFilter(loglvl)
    logger.addFilter(filt)

    # handlers
    # no need to call hdlr.createLock(), it is called in hdlr.__init__()
    hdlr = logging.handlers.TimedRotatingFileHandler(filename, when='d')
    fmtr = logging.Formatter(fmt, datefmt)

    hdlr.setFormatter(fmtr)
    logger.addHandler(hdlr)

    _HAS_INIT = True


#------------------------------------------------------------------------------
#   SysLogger filter
#------------------------------------------------------------------------------
class SysFilter(logging.Filter):
    def __init__(self, level, name=''):
        # be careful for super()
        super(SysFilter, self).__init__(name)
        self.logLevel = level

    def filter(self, record):
        if record.levelno & self.logLevel :
            return True
        return False
#------------------------------------------------------------------------------
#   SysLogger class
#------------------------------------------------------------------------------
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
        apply(self._log, (WARNING, msg, args), kwargs)



# ----------------------------------------------------------------------------
_default_filter    = SysFilter(DEFAULT_LOG_LEVEL)
_default_formatter = logging.Formatter(DEFAULT_LOG_FORMAT, DEFAULT_TIME_FORMAT)
_default_handler   = logging.StreamHandler(sys.stderr)

logging.setLoggerClass(SysLogger)
logger = logging.getLogger('kitty')
logger.setLevel(DEBUG)
logger.addFilter(_default_filter)

_default_handler.setFormatter(_default_formatter)
logger.addHandler(_default_handler)

# -----------------------------------------------------------------------------
#    test
# -----------------------------------------------------------------------------
def test():
    init('test.log')

    logger.debug("this is debug")
    logger.notice("this is notice")
    logger.trace("this is trace")
    logger.warning("this is warning")
    logger.fatal("this is fatal")

if __name__ == '__main__':
    test()
