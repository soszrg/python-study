# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def co_routine():
    print "start"
    x = yield 1
    print "recieve==>", x
    y = yield 2
    z = yield 3
    print "recieve==>", y, z