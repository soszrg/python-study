# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
from threading import Thread, Semaphore

import time

semaphore = Semaphore(3)


class SemaphoreThread(Thread):
    def __init__(self, tid):
        super(SemaphoreThread, self).__init__()
        self.tid = tid

    def run(self):
        while True:
            with semaphore:
                wt = random.randint(1, 5)
                print "{} acquire semaphore:{}".format(self.tid, wt)
                time.sleep(wt)
                print "{} release semaphore".format(self.tid)


if __name__ == "__main__":
    threads = []
    for i in range(5):
        trd = SemaphoreThread(i)
        trd.start()
        threads.append(trd)

    for t in threads:
        t.join()

