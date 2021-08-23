#%%
import random
import multiprocessing
import sys
import time


def generate_something():
    return random.choice(range(10))


def f(event):
    while True:
        x = generate_something()
        print("Value is ", x)
        if x == 5:
            print("Got what I am searching for.")
            event.set()
        time.sleep(0.5)


if __name__ == "__main__":

    jobs = []
    # Create Event
    event = multiprocessing.Event()

    # Create two processes
    for i in range(2):
        p = multiprocessing.Process(target=f, args=(event,))
        p.start()
        jobs.append(p)

    # Check whether event is set or not
    # When set close all child processes
    while True:
        if event.is_set():
            print("Exiting all child processess..")
            for i in jobs:
                # Terminate each process
                i.terminate()
            # Terminating main process
            sys.exit(1)
        time.sleep(2)

# %%
