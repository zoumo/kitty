#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
To use, simply 'import utils' and pylog.init(filename)
based on logging
"""

import os, sys, time
# sign.so
import sign

# __all__ = ['empty']

__author__  = "Jim Zhang"
__status__  = "production"
# Note: the attributes below are no longer maintained.
__version__ = "0.1.0.0"
__date__    = "24/08/2014"

# -----------------------------------------------------------------------------
#    function
# -----------------------------------------------------------------------------
def empty(obj) :
    """
    if obj is False | 0 | "" | None | [] | () | {}
    return False
    """
    if not obj :
        return True
    else :
        return False

def sign_fs64(text):
    """
    计算文本的fs64签名
    """
    (flag, high, low) = sign.fs64(text)
    #return ((low << 32) + high)
    # return ((high << 32) + low)
    return (high, low)

# def getTimeSuffix(split = False, kind = 'day'):
#     if split == False:
#         return ""

#     fmt = {
#         'day'  : '%Y%m%d',
#         'hour' : '%Y%m%d%H',
#         'min'  : '%Y%m%d%H%M',
#     }

#     return "." + time.strftime(fmt[kind], time.localtime(time.time()))


# -----------------------------------------------------------------------------
#    test
# -----------------------------------------------------------------------------
def test():
    pass

if __name__ == '__main__':
    test()




