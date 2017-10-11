# coding: utf-8
from threading import Timer


class TimerTest(object):

    def __init__(self):
        self.t = None

    def fun(self):
        print "hello, world"
        self.t = Timer(5.0, self.fun)
        self.t.setDaemon(True)
        self.t.start()

    def threadd(self):
        self.t = Timer(5.0, self.fun)
        self.t.setDaemon(True)
        self.t.start()

# if __name__ == "__main__":
#     TimerTest()