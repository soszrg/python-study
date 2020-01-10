import multiprocessing as mp
import threading as td
import time


class Data(object):
    g = 1


def job(obj, process_id, delta=1):
    while True:
        print(f"[{process_id}] g==>{obj.g}")
        time.sleep(delta)


if __name__ == "__main__":
    p1 = mp.Process(target=job, args=(1,))
    p1.start()

    Data.g = 2
    p2 = mp.Process(target=job, args=(2, 3))
    p2.start()

    p1.join()
    p2.join()
