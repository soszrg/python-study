# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from multiprocessing.managers import BaseManager

host = '127.0.0.1'
port = 8050
secret = 'secret'

shared_list = ["zrg"]


class RemoteManager(BaseManager):
    pass

RemoteManager.register(typeid=str('zrg_test'), callable=lambda: shared_list)
mgr = RemoteManager(address=(host, port), authkey=secret)
server = mgr.get_server()
server.serve_forever()

