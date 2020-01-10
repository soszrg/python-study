import multiprocessing as mp
import threading as td
import time


class Data(object):
    g = 1


def job(process_id, delta=1):
    while True:
        print(f"[{process_id}] g==>{Data.g}")
        if process_id == 2:
            Data.g = process_id
        time.sleep(delta)


if __name__ == "__main__":
    t1 = td.Thread(target=job, args=(1,))
    t1.start()

    Data.g = 2
    t2 = td.Thread(target=job, args=(2, 3))
    t2.start()

    t1.join()
    t2.join()
