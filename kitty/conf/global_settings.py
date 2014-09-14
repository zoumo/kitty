#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

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
