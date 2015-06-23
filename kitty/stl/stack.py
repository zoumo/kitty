#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stack
"""

import os
import sys
import time


# ----------------------------------------------------------------------------
#    class
# ----------------------------------------------------------------------------
class Stack:

    def __init__(self):
        self._stack = []

    def size(self):
        return len(self._stack)

    def empty(self):
        length = len(self._stack)
        return True if length == 0 else False

    def pop(self):
        return self._stack.pop()

    def push(self, item):
        self._stack.append(item)

    def top(self):
        return self._stack[-1]

# ----------------------------------------------------------------------------
#    test
# ----------------------------------------------------------------------------


def test():
    pass

if __name__ == '__main__':
    test()
