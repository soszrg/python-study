# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import random
from threading import Thread, Condition, Lock

import time

import datetime
lock = Lock()
condition = Condition(lock)
counter = []


class ConsumerThread(Thread):

    def __init__(self, tid):
        super(ConsumerThread, self).__init__()
        self.tid = tid

    def run(self):
        while True:
            print "consumer ready acquire[%s]" % str(datetime.datetime.now())
            if condition.acquire():
                condition.wait()
                print "{} consume condition:{}".format(self.tid, counter)
                counter.pop()
                condition.release()


class ProducerThread(Thread):

    def __init__(self, tid=1):
        super(ProducerThread, self).__init__()
        self.tid = tid

    def run(self):
        while True:
            if condition.acquire():
                wt = random.randint(1, 3)
                time.sleep(wt)
                counter.append(wt)
                print "{} product condition:{}".format(self.tid, counter)
                condition.notify()
                condition.release()

if __name__ == '__main__':
    consumer = ConsumerThread(tid='c1')
    consumer.start()

    consumer1 = ConsumerThread(tid='c2')
    consumer1.start()

    consumer2 = ConsumerThread(tid='c3')
    consumer2.start()

    producer = ProducerThread()
    producer.start()
    producer.join()
    consumer.join()
    consumer1.join()
    consumer2.join()
