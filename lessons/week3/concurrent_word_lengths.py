# Using multi-threading to compute word lengths concurrently.

import threading
from time import sleep
from random import seed, uniform

words = ['goldfish', 'zoology', 'mirth', 'car',
         'promenade', 'home', 'flashlight', 'office']

# 1) Describe what each thread does.
def worker():
    sleep(uniform(1, 10))  # Pretend each thread uses lots of time.
    i = int(threading.current_thread().name)
    length_i = len(words[i])
    msg = "Thread {}: length of '{}' is {}\n".format(i, words[i], length_i)
    print(msg, end='')

# 2) Create the threads.
threads = [threading.Thread(target=worker, name=str(i))
           for i in range(len(words))]

# 3) Start them running.
seed()
for t in threads:
    t.start()

# 4) To ensure a particular thread, or every thread, has finished, use join():
for t in threads:
    t.join()
print("Every thread has finished.")
