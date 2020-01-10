# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from multiprocessing.managers import BaseManager

host = '127.0.0.1'
port = 8050
secret = 'secret'

shared_list = []


class RemoteManager(BaseManager):
    pass

RemoteManager.register(str('zrg_test'))
mgr = RemoteManager(address=(host, port), authkey=secret)
mgr.connect()

l = mgr.zrg_test()
l.append(1)
