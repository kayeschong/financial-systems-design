# Our third attempt to find the maximum length of the words in a list
# via multi-threading.

import threading

words = ['goldfish', 'zoology', 'mirth', 'car',
         'promenade', 'home', 'flashlight', 'office']
max_length = 0

def worker():
    global max_length
    length_i = len(threading.current_thread().name)
    with max_length_lock:
        # Thanks to this with statement, the following logic will work:
        if length_i <= 4:
            print('Length is too short, not bothering to update max_length')
            return
        if length_i > max_length:
            max_length = length_i

max_length_lock = threading.Lock()

threads = [threading.Thread(target=worker, name=w) for w in words]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Maximum word length:", max_length)
