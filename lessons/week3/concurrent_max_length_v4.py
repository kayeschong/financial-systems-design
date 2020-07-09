# Our fourth attempt to find the maximum length of the words in a list
# via multi-threading.

import threading
from functools import reduce

words = ['goldfish', 'zoology', 'mirth', 'car',
         'promenade', 'home', 'flashlight', 'office']

def worker():
    global lengths
    i = int(threading.current_thread().name)
    # No other thread is trying to modify this *element* of lengths,
    # so there is no need for a lock.
    lengths[i] = len(words[i])

lengths = [0] * len(words)

threads = [threading.Thread(target=worker, name=str(i))
           for i in range(len(words))]

for t in threads:
    t.start()

for t in threads:
    t.join()

# (All the above code is really just a thread-based version of:
# lengths = [len(w) for w in words]
# )

# Having performed the Map, we now Reduce:
max_length = reduce(max, lengths)

print("Maximum word length:", max_length)
