#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

__author__ = "Jim Zhang"
VERSION = (1, 0, 0, 'alpha', 0)


def get_version(*args, **kwargs):
    # Avoid circular import
    from kitty.utils.version import get_version
    return get_version(*args, **kwargs)


def setup(app_name='kitty', settings_module=""):

    from kitty.utils import log
    from kitty.conf import KITTY_SETTINGS_MODULE, settings

    os.environ.setdefault(KITTY_SETTINGS_MODULE, settings_module)

    if not app_name:
        app_name = 'kitty'

    if not os.path.isdir(settings.LOG_PATH):
        os.mkdir(settings.LOG_PATH)

    LOG_CONFIG = {
        'name': app_name,
        'filename': settings.LOG_PATH + "/" + app_name + ".log",
        'level': settings.LOG_LEVEL
    }

    log.getLogger(**LOG_CONFIG)

# ----------------------------------------------------------------------
#   conf
# ----------------------------------------------------------------------
__version__ = get_version(VERSION)
