#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, argparse
from os.path import dirname, realpath

try:
    # install
    import kitty
except ImportError, e:
    #local
    sys.path.append(dirname(dirname(dirname(realpath(__file__)))))
    import kitty



def opt_parse():
    parser = argparse.ArgumentParser(description='this is a test')

    args = parser.parse_args()
    return args

if __name__ == "__main__" :
    # print opt_parse()

    # logger.debug("this is debug")
    # logger.notice("this is notice")
    # logger.trace("this is trace")
    # logger.warning("this is warning")
    # logger.fatal("this is fatal")

    # print empty(logger)
    # print empty({})

    
    kitty.setup("kitty.test.setting")
    # kitty.setup()
    
    from kitty.conf import settings
    from kitty.utils.log import getLogger
    from kitty.utils.function import empty
    from kitty.utils.log import root
    print "app name ",  settings.APP_NAME

    logger = getLogger(settings.APP_NAME)
    print "logger name ", logger.name
    print "logger parent name ", logger.parent.name
    # print settings.SETTINGS_MODULE
    # print dir(settings)
    print empty([])
    print empty("123")