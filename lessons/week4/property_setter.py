class Celsius:
    def __init__(self, temp):
        self.temperature = temp  # Invokes the code below (!).

    @property
    def temperature(self):
        return self._temp

    @temperature.setter
    def temperature(self, value):
        if value < -273:
            raise ValueError("Too cold")
        self._temp = value


if __name__ == "__main__":
    c = Celsius(20)
    print('Temperature is now: ', c.temperature)
    print()

    c.temperature = 25
    print('Temperature is now: ', c.temperature)
    print()

    c.temperature = -300
    print('Temperature is now: ', c.temperature)
