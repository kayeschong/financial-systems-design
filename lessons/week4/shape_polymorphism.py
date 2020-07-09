from math import pi


class Shape:
    # There are no instance variables.
    def area(self):
        # "In user defined base classes, abstract methods should raise
        # NotImplementedError when they require derived classes to override
        # the method [...]."
        raise NotImplementedError("Non-specific Shape, area is undefined")


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return pi * self.radius * self.radius


class Triangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height / 2.


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


class Square(Rectangle):  # Notice the base class here.
    def __init__(self, length):
        self.length = length
        # self.width = length

    def area(self):
        return self.length * self.length


if __name__ == "__main__":
    # Notice that Python calls __init__() for us:
    shapes = [Circle(5), Triangle(2, 3), Square(8), Rectangle(4, 9)]
    print("Are they all Shapes?", all([isinstance(s, Shape) for s in shapes]))
    # Polymorphism: Python figures out which version of area() to call!
    areas = [s.area() for s in shapes]
    print("Areas of shapes:", areas)
