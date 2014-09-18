#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

__author__  = "Jim Zhang"
VERSION = (1, 0, 0, 'alpha', 0)

def get_version(*args, **kwargs):
    # Avoid circular import
    from kitty.utils.version import get_version
    return get_version(*args, **kwargs)

def setup(settings_module=""):

    from kitty.utils import log
    from kitty.conf import KITTY_SETTINGS_MODULE, settings

    os.environ.setdefault(KITTY_SETTINGS_MODULE, settings_module)

    log_file = settings.LOG_PATH + "/" + settings.APP_NAME + ".log"

    if not os.path.isdir(settings.LOG_PATH):
        os.mkdir(settings.LOG_PATH)

    #init logger
    log.getLogger(name=settings.APP_NAME, filename=log_file, level=settings.LOG_LEVEL)

#---------------------------------------------------------------------------
#   conf
#---------------------------------------------------------------------------
__version__ = get_version(VERSION)

#---------------------------------------------------------------------------
#   test
#---------------------------------------------------------------------------
def opt_parse():
    # Command-line option and argument parsing library
    # https://docs.python.org/dev/library/argparse.html
    import argparse
    parser = argparse.ArgumentParser(description='this is a spider')
    parser.add_argument('file',
                        help='query list file path')
    parser.add_argument('-p', action='store', dest='velocity', type=int, default=20,
                        help='request velocity(per second), default 20')
    args = parser.parse_args()
    return args


if __name__ == "__main__" :
    args = opt_parse()