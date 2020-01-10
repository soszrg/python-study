# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from multiprocessing import Pool as ProcessPool, freeze_support, Process, current_process
from multiprocessing.dummy import Pool as ThreadPool
import time


def wrapper(func):
    def inter(*arg, **kwargs):
        start = time.time()
        func(*arg, **kwargs)
        end = time.time()
        print("Take {}\n".format(str(end - start)))

    return inter


# @wrapper
def func(x):
    print(current_process().pid)
    for _ in range(10000000):
        x += 1
    print("4: %d" % x)
    # time.sleep(3)
    return x


def callback(x):
    print("3: %d" % x)


if __name__ == '__main__':
    freeze_support()
    # p = Process(target=func, kwargs={"x": 10})
    # p.start()
    # print "wait subprocess exit..."
    # p.join()
    # print "main exit!"
    start = time.time()
    # pp = ProcessPool(2)
    pp = ThreadPool(2)
    pp.map_async(func, [1000, 3])
    # ret = pp.apply_async(func, args=(10, ), callback=callback)
    # print "1: %d" % ret.get()
    # print "wait subprocess exit..."
    # time.sleep(5)
    pp.close()
    pp.join()
    # tp = ThreadPool(2)
    # tp.map_async(func, [1000, 3])
    # tp.close()
    # tp.join()
    print("main exit:%s" % (time.time() - start))
