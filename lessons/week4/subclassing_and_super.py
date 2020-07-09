class Person:
   def __init__(self, first_name, last_name, age):
      self.first_name = first_name
      self.last_name = last_name
      self.age = age

   def __str__(self):
      return self.first_name + ' ' + self.last_name + ', ' + str(self.age)


class Employee(Person):
    def __init__(self, first_name, last_name, age, id_num):
        super().__init__(first_name, last_name, age)
        self.id_num = id_num

    def __str__(self):
        return super().__str__() + ', ' + str(self.id_num)


if __name__ == "__main__":
    people = [Person('Adam', 'Smith', 25),
              Employee('Margaret', 'Jones', 30, 12345)]
    for p in people:
        print(p)
