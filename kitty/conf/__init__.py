#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

import importlib
import time     # Needed for Windows

from kitty.conf import global_settings

#---------------------------------------------------------------------------
#   conf init
#---------------------------------------------------------------------------
class Settings(object):

    def __init__(self, settings_module):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        try:
            mod = importlib.import_module(self.SETTINGS_MODULE)
        except ImportError as e:
            raise ImportError(
                "Could not import settings '%s' (Is it on sys.path? Is there an "
                "import error in the settings file?): %s"
                % (self.SETTINGS_MODULE, e)
            )

        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)


    def is_overridden(self, setting):
        return setting in self._explicit_settings


settings = Settings()
#---------------------------------------------------------------------------
#   test
#---------------------------------------------------------------------------


if __name__ == "__main__" :
    pass