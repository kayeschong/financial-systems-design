# Our first attempt to find the maximum length of the words in a list
# via multi-threading.

import threading

words = ['goldfish', 'zoology', 'mirth', 'car',
         'promenade', 'home', 'flashlight', 'office']
max_length = 0

# The GIL ("Global Interpreter Lock") in CPython does *not* eliminate the
# "race condition" in the following code when accessing and updating
# max_length -- see Lesson 38 in _Effective Python_ by Brett Slatkin.
# I.e. Even using CPython, this code is not acceptable and must be rewritten.
def worker():
    global max_length
    length_i = len(threading.current_thread().name)
    if length_i > max_length:
        max_length = length_i

threads = [threading.Thread(target=worker, name=w) for w in words]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Maximum word length:", max_length)
