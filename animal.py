class Animal:
    def __init__(self) -> None:
        self.name = "Animal"
        self.age = 0

    def walk(self):
        print("I'm walking")


class Dog(Animal):
    def bark(self):
        print("Woof")
