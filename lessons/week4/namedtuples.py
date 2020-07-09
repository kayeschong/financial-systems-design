from collections import namedtuple

Car = namedtuple('Car','colour miles')
c = [Car(colour='silver', miles=60000),  # Syntax 1
     Car('red', 30000),  # Syntax 2
     Car('black', 50000)]

# Named tuples are read-only:
c[0].miles = 105000  # Will not work.

# With ordinary tuples you would need to use subscripts;
# this is more readable:
[car for car in c if car.miles > 50000]

# When we need an "anonymous function", we can write either
from operator import attrgetter
sorted(c, key=attrgetter('miles'))
# or
sorted(c, key=lambda car: car.miles)
# versus (using ordinary tuples):
# sorted(c, key=lambda car: car[1])
