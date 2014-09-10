#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))
from conf import *


def opt_parse():
    parser = argparse.ArgumentParser(description='this is a test')

    args = parser.parse_args()
    return args

if __name__ == "__main__" :
    print utils.sign_fs64("zhangjun17")
    print opt_parse()

    pylogger.debug("this is debug")
    pylogger.notice("this is notice")
    pylogger.trace("this is trace")
    pylogger.warning("this is warning")
    pylogger.fatal("this is fatal")

    print utils.empty(pylogger)
    print utils.empty({})
    