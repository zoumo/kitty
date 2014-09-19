#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Settings and configuration for Django.

Values will be read from the module specified by the DJANGO_SETTINGS_MODULE environment
variable, and then from kitty.conf.global_settings; see the global settings file for
a list of all possible variables.
"""
import os, sys

import importlib

from kitty.conf import global_settings
from kitty.core.exceptions import ImproperlyConfigured
from kitty.utils.functional import LazyObject, empty
from kitty.utils import six
from kitty.utils.log import root as logger


KITTY_SETTINGS_MODULE = "KITTY_SETTINGS_MODULE"
DEFAULT_SETTINGS_MODULE = "kitty.conf.global_settings"

class LazySettings(LazyObject):
    """
    A lazy proxy for either global settings or a custom settings object.
    The user can manually configure settings prior to using them. Otherwise,
    kitty uses the settings module pointed to by KITTY_SETTINGS_MODULE.
    """

    def _setup(self, name=None):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        settings_module = os.environ.get(KITTY_SETTINGS_MODULE)
        if not settings_module:
            desc = ("setting %s" % name) if name else "settings"
            # raise ImproperlyConfigured(
            #     "Requested %s, but settings are not configured. "
            #     "You must either define the environment variable %s "
            #     "or call settings.configure() before accessing settings."
            #     % (desc, KITTY_SETTINGS_MODULE))
            logger.warning("Requested [%s], but settings are not configured. use default settings [%s]", desc, DEFAULT_SETTINGS_MODULE)
        else:
            desc = ("setting %s" % name) if name else "settings"
            logger.notice("requested [%s] is lazy initialized  in settings module [%s]", desc, settings_module)

        self._wrapped = Settings(settings_module)

    # def __getattr__(self, name):
    #     if self._wrapped is empty:
    #         self._setup(name)
    #     return getattr(self._wrapped, name)

    def configure(self, default_settings=global_settings, **options):
        """
        Called to manually configure the settings. The 'default_settings'
        parameter sets where to retrieve any unspecified values from (its
        argument must support attribute access (__getattr__)).
        """
        if self._wrapped is not empty:
            raise RuntimeError('Settings already configured.')
        holder = UserSettingsHolder(default_settings)
        for name, value in options.items():
            setattr(holder, name, value)
        self._wrapped = holder

    @property
    def configured(self):
        """
        Returns True if the settings have already been configured.
        """
        return self._wrapped is not empty

class BaseSettings(object):
    """
    this is the basic setting object
    it is used to check the format by __setattr__
    """

    SETTINGS_MODULE = DEFAULT_SETTINGS_MODULE

    def __setattr__(self, name, value):
        if name in ("MEDIA_URL", "STATIC_URL") and value and not value.endswith('/'):
            raise ImproperlyConfigured("If set, %s must end with a slash" % name)
        object.__setattr__(self, name, value)

class Settings(BaseSettings):

    def __init__(self, settings_module=None):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        self._explicit_settings = set()

        # not follows -- None | "" | False
        if settings_module :
            # store the settings module in case someone later cares
            self.SETTINGS_MODULE = settings_module
            try:
                mod = importlib.import_module(self.SETTINGS_MODULE)
            except ImportError as e:
                raise ImportError(
                    "Could not import settings [%s] (Is it on sys.path? Is there an "
                    "import error in the settings file?): %s"
                    % (self.SETTINGS_MODULE, e)
                )

            for setting in dir(mod):
                if setting.isupper():
                    setting_value = getattr(mod, setting)
                    setattr(self, setting, setting_value)
                    self._explicit_settings.add(setting)


    def is_overridden(self, setting):
        return setting in self._explicit_settings

class UserSettingsHolder(BaseSettings):
    """
    Holder for user configured settings.
    """
    # SETTINGS_MODULE doesn't make much sense in the manually configured
    # (standalone) case.
    # SETTINGS_MODULE = None

    def __init__(self, default_settings):
        """
        Requests for configuration variables not in this class are satisfied
        from the module specified in default_settings (if possible).
        """
        self.__dict__['_deleted'] = set()
        self.default_settings = default_settings

    def __getattr__(self, name):
        if name in self._deleted:
            raise AttributeError
        return getattr(self.default_settings, name)

    def __setattr__(self, name, value):
        self._deleted.discard(name)
        super(UserSettingsHolder, self).__setattr__(name, value)

    def __delattr__(self, name):
        self._deleted.add(name)
        if hasattr(self, name):
            super(UserSettingsHolder, self).__delattr__(name)

    def __dir__(self):
        return list(self.__dict__) + dir(self.default_settings)

    def is_overridden(self, setting):
        deleted = (setting in self._deleted)
        set_locally = (setting in self.__dict__)
        set_on_default = getattr(self.default_settings, 'is_overridden', lambda s: False)(setting)
        return (deleted or set_locally or set_on_default)


settings = LazySettings()
#---------------------------------------------------------------------------
#   test
#---------------------------------------------------------------------------


if __name__ == "__main__" :
    pass