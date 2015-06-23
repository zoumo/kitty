#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import argparse
from os.path import dirname, realpath

try:
    # install
    import kitty
except ImportError, e:
    # local
    sys.path.append(dirname(dirname(dirname(realpath(__file__)))))
    import kitty


def opt_parse():
    parser = argparse.ArgumentParser(description='this is a test')

    args = parser.parse_args()
    return args


def test_conf():
    app_name = 'test'
    kitty.setup(app_name, "kitty.test.settings")
    # kitty.setup()

    from kitty.conf import settings
    from kitty.utils.log import getLogger
    from kitty.utils.function import empty
    from kitty.utils.log import root

    print settings.is_overridden('LOG_PATH')
    print 'TEST_CONF' in settings._wrapped._explicit_settings

    logger = getLogger(app_name)

    print "app name", app_name
    print "logger name ", logger.name
    print "logger parent name ", logger.parent.name

if __name__ == "__main__":
    test_conf()
()
