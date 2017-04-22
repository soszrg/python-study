# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
from threading import Thread, Lock

import time


class LockThread(Thread):
    lock = Lock()

    def __init__(self, tid):
        super(LockThread, self).__init__()
        self.tid = tid

    def run(self):
        with self.lock:
            wt = random.randint(1, 5)
            print "{} acquire lock:{}".format(self.tid, wt)
            time.sleep(wt)
            print "{} release lock".format(self.tid)

if __name__ == '__main__':
    threads = []
    for i in range(5):
        trd = LockThread(i+1)
        trd.start()
        threads.append(trd)

    for t in threads:
        t.join()

