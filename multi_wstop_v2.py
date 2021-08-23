#%%
import os
from datetime import datetime
from multiprocessing import Process, Event


def worker(range_, target, found_event):
    print("{} | pid: {} started".format(datetime.now(), os.getpid()))
    for x in range_:
        if x == target:
            print("{} | pid: {} found target".format(datetime.now(), os.getpid()))
            found_event.set()


if __name__ == "__main__":

    N_WORKERS = 4

    step = int(200e6)
    ranges = [range(x, x + step) for x in range(0, N_WORKERS * step, step)]  # change `range` to `xrange` for Python 2
    # range(0, 200000000), ..., range(800000000, 1000000000)]
    target = int(150e6)  # <-- worker finding this value triggers massacre
    found_event = Event()

    pool = [Process(target=worker, args=(range_, target, found_event)) for range_ in ranges]

    for p in pool:
        p.start()

    found_event.wait()  # <- blocks until condition met
    print("{} | terminating processes".format(datetime.now()))
    for p in pool:
        p.terminate()
    for p in pool:
        p.join()
    print("{} | all processes joined".format(datetime.now()))

# %%
