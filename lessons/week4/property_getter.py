from math import sqrt

class RightTriangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    @property
    def hypotenuse(self):
        return sqrt(self.height**2 + self.width**2)


if __name__ == "__main__":
    # If we get here, then someone is executing this script
    # rather than importing it.
    rt = RightTriangle(3, 4)
    print('Height: {}, width: {}, hypotenuse: {}'
          .format(rt.height,  # Instance variables are not private...
                  rt.width,
                  rt.hypotenuse))  # N.B. Same syntax as for height and width.
    print()

    rt.height = 5   # ...and not immutable either.
    rt.width = 12
    print('Height: {}, width: {}, hypotenuse: {}'
          .format(rt.height, rt.width, rt.hypotenuse))
