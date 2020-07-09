# Using radix sort to explore the tradeoff between "Pythonic" code
# versus efficient code.
# Original version: https://stackoverflow.com/questions/33901534/radix-sort-program-in-python

from random import randint
from math import log10, ceil
from more_itertools import bucket
import timeit


def radix_sort(A, max_digits):
    """More elegant, but far too slow due to the call to bucket()."""
    radix_keys = list(map(str, range(10)))
    B = [str(a_i).zfill(max_digits) for a_i in A]
    for digit_index in range(-1, -max_digits-1, -1):
        buckets = bucket(B, key=lambda b_i: b_i[digit_index])
        B = []
        for j in radix_keys:
            B.extend(buckets[j])
    return [int(b_i) for b_i in B]


def radix_sort_2(A, max_digits):
    """Less elegant, but much faster with the call to bucket() removed."""
    radix_keys = list(map(str, range(10)))
    B = [str(a_i).zfill(max_digits) for a_i in A]
    for digit_index in range(-1, -max_digits-1, -1):
        buckets = {i: [] for i in radix_keys}
        for b_i in B:
            buckets[b_i[digit_index]].append(b_i)
        B = []
        for j in radix_keys:
            B.extend(buckets[j])
    return [int(b_i) for b_i in B]


def sample_input(list_length):
    max_value = 10 * list_length - 1
    max_digits = ceil(log10(max_value))
    A = [randint(1, max_value) for _ in range(list_length)]
    return A, max_digits


list_length = 1000000  # Could be a command line input. Must be a power of 10.
num_trials = 5  # Could be a a command line input.

straw_man_cmd = 'sorted(sample_input({})[0])'.format(list_length)
straw_man_time = timeit.timeit(straw_man_cmd,
                               setup="from __main__ import sample_input",
                               number=num_trials)
print('Built-in sort: ' + str(straw_man_time))

# radix_sort_cmd = 'radix_sort(*sample_input({}))'.format(list_length)
# radix_sort_time = timeit.timeit(radix_sort_cmd,
#                                 setup="from __main__ import sample_input, radix_sort",
#                                 number=num_trials)
# print('Radix sort: ' + str(radix_sort_time))

radix_sort_2_cmd = 'radix_sort_2(*sample_input({}))'.format(list_length)
radix_sort_2_time = timeit.timeit(radix_sort_2_cmd,
                               setup="from __main__ import sample_input, radix_sort_2",
                               number=num_trials)
print('Radix sort: ' + str(radix_sort_2_time))
