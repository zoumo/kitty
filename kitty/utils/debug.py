#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-06-30 19:40:25
# @Author  : Jim Zhang (jim.zoumo@gmail.com)
# @Github  : https://github.com/zoumo

import time
import sys


def func_timer(func):
    def timer(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print >> sys.stderr, "%s use %f time" % (func.__name__, end-start)
        return result
    return timer
