#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys



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

# sys.path.append(ROOT_PATH)
# sys.path.append(LIB_PATH)
# sys.path.append(CONF_PATH)

# user definded logger


# user definded functions
# import kitty.utils

def setup(app_name, root_path):
    import kitty.log
    import kitty.conf

    log_path = root_path + "/log"
    log_file = log_path + "/" + app_name + ".log"
    if not os.path.isdir(log_path):
        os.mkdir(log_path)

    kitty.log.init(log_file)


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