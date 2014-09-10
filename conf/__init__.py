#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

__all__ = ['ROOT_PATH', 'CONF_PATH', 'LOG_PATH', 'BIN_PATH', 'DATA_PATH', 'LIB_PATH',
           'pylog', 'pylogger', 'utils', 'argparse']

__author__  = "Jim Zhang"
__status__  = "production"
# Note: the attributes below are no longer maintained.
__version__ = "0.1.0.0"
__date__    = "24/08/2014"

#---------------------------------------------------------------------------
#   conf init
#---------------------------------------------------------------------------

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CONF_PATH = ROOT_PATH + "/conf"
LOG_PATH  = ROOT_PATH + "/log"
BIN_PATH  = ROOT_PATH + "/bin"
DATA_PATH = ROOT_PATH + "/data"
LIB_PATH  = ROOT_PATH + "/lib"

sys.path.append(LIB_PATH)
sys.path.append(CONF_PATH)

# user definded logger
import pylog
pylog.init(LOG_PATH + "/spider.log")
# must imprt pylogger after init()
from pylog import pylogger

# user definded functions
import utils

# Command-line option and argument parsing library
# https://docs.python.org/dev/library/argparse.html
import argparse

#---------------------------------------------------------------------------
#   test
#---------------------------------------------------------------------------
def opt_parse():
    parser = argparse.ArgumentParser(description='this is a spider')
    parser.add_argument('file',
                        help='query list file path')
    parser.add_argument('-p', action='store', dest='velocity', type=int, default=20,
                        help='request velocity(per second), default 20')
    args = parser.parse_args()
    return args


if __name__ == "__main__" :
    pass