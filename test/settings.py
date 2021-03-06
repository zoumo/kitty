#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

# realpath will eliminate any symbolic links encountered in the path
# abspath only return a normalized absolutized version of the pathname path
# BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_PATH = BASE_PATH
LOG_PATH = ROOT_PATH + "/test"
TEST_CONF = "TEST"

DEBUG = False

# Default content type and charset to use for all HttpResponse objects, if a
# MIME type isn't manually specified. These are used to construct the
# Content-Type header.
DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'

# Encoding of files read from disk (template and initial SQL files).
FILE_CHARSET = 'utf-8'

# Email address that error messages come from.
SERVER_EMAIL = 'root@localhost'
