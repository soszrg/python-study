# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool

import time


def wrapper(func):
    def inter(*arg, **kwargs):
        start = time.time()
        func(*arg, **kwargs)
        end = time.time()
        print "Take {}\n".format(str(end-start))

    return inter


def func(x):
    for _ in range(1000000):
        x += 1
    return x

pp = ProcessPool()
pp.map(func, [1000, ])

# tp = ThreadPool(2)
# tp.map(func, [1000, 32345])


