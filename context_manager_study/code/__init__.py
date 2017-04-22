# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class MyContext(object):
    def __init__(self, a=1):
        self.a = a

    def __enter__(self):
        self.a += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        print self.a


if __name__ == '__main__':
    context = MyContext(3)
    file
    with context:
        print "===test==="

    print "===end==="
