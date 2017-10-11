# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from functools import wraps


def register():
    print "decorate %s" % func

    @wraps(func)
    def aaa(x, y):
        print func.__name__
        func(x, y)
    return aaa


@register()
def func(x, y):
    print "running func"


def make_average():
    def averager(x):
        store = [0, 0]
        store[0] += x
        store[1] += 1
        return store[0]/store[1]

    return averager

print func.__name__
func(y=2, x=1)
averager = make_average()
averager(1)
