# The "coin change problem" from
# https://www.hackerrank.com/challenges/coin-change/problem .

# lru_cache is Python's built-in mechanism for "memoisation".
from functools import lru_cache


@lru_cache(maxsize=1000000)  # Try commenting this out.
def getWaysHelper(n, c_sorted):
    c_largest = c_sorted[0]
    if len(c_sorted) == 1:
        return 1 if n % c_largest == 0 else 0
    if c_largest > n:
        return getWaysHelper(n, c_sorted[1:])
    # Recursion based on using c_largest zero times:
    sub_result_1 = getWaysHelper(n, c_sorted[1:])
    if n == c_largest:
        # We can make change by using the largest value exactly once.
        sub_result_2 = 1
    else:
        sub_result_2 = getWaysHelper(n - c_largest, c_sorted)
    return sub_result_1 + sub_result_2


def getWays(n, c):
    return getWaysHelper(n, tuple(sorted(c, reverse=True)))


def runEasyTestCases():
    print('About to run easy test cases...')
    assert getWays(10, [5, 2]) == 2
    assert getWays(4, [1, 2, 3]) == 4
    assert getWays(3, [8, 3, 2, 1]) == 3
    assert getWays(10, [2, 5, 3, 6]) == 5
    assert getWays(2,
                   [44, 5, 9, 39, 6, 25, 3, 28, 16, 19, 4, 49, 40, 22,
                    2, 12, 45, 33, 23, 42, 34, 15, 46, 26, 13, 31, 8]) == 1
    assert getWays(75,
                   [25, 10, 11, 29, 49, 31, 33, 39, 12, 36, 40, 22, 21,
                    16, 37, 8, 18, 4, 27, 17, 26, 32, 6, 38, 2, 30, 34]) == 16694


def runHardTestCase():
    print('About to run hard test case...')
    assert getWays(166,
                   [5, 37, 8, 39, 33, 17, 22, 32, 13, 7, 10, 35,
                    40, 2, 43, 49, 46, 19, 41, 1, 12, 11, 28]) == 96190959


def main():
    runEasyTestCases()
    runHardTestCase()
    print('Passed all test cases.')


main()
