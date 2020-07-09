# Transforming a 3x3 matrix of integers into a "magic square"
# by performing the least costly series of replacements.  From
# https://www.hackerrank.com/challenges/magic-square-forming/problem .

# The key insight is that
# 1) the problem only requires us to handle the 3x3 case, and
# 2) there are only 8 possible 3x3 magic squares, namely:
All3x3Squares = [[[8, 1, 6], [3, 5, 7], [4, 9, 2]],
                 [[6, 1, 8], [7, 5, 3], [2, 9, 4]],
                 [[4, 9, 2], [3, 5, 7], [8, 1, 6]],
                 [[2, 9, 4], [7, 5, 3], [6, 1, 8]],
                 [[8, 3, 4], [1, 5, 9], [6, 7, 2]],
                 [[4, 3, 8], [9, 5, 1], [2, 7, 6]],
                 [[6, 7, 2], [1, 5, 9], [8, 3, 4]],
                 [[2, 7, 6], [9, 5, 1], [4, 3, 8]]]


def distanceMetric(square1, square2):
    return (abs(square1[0][0] - square2[0][0]) +
            abs(square1[0][1] - square2[0][1]) +
            abs(square1[0][2] - square2[0][2]) +
            abs(square1[1][0] - square2[1][0]) +
            abs(square1[1][1] - square2[1][1]) +
            abs(square1[1][2] - square2[1][2]) +
            abs(square1[2][0] - square2[2][0]) +
            abs(square1[2][1] - square2[2][1]) +
            abs(square1[2][2] - square2[2][2]))


def formingMagicSquare(square):
    return min([distanceMetric(square, valid) for valid in All3x3Squares])


def runTestCases():
    assert formingMagicSquare([[5, 3, 4], [1, 5, 8], [6, 4, 2]]) == 7
    assert formingMagicSquare([[4, 8, 2], [4, 5, 7], [6, 1, 6]]) == 4


def main():
    runTestCases()
    print('Passed all test cases.')


main()
