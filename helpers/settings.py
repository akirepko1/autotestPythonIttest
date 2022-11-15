# -*- coding: utf-8 -*-
"""
Parent file with settings, can be override by local_settings
"""

SCREEN_ERROR_PATH = 'screenshot-error/'

SHORT_WAIT = 5
LONG_WAIT = 120
PAGE_TIMEOUT = 90

try:
    from .local_settings import *
except ImportError:
    pass
