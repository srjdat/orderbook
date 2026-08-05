class Test:
    _age: int

    def __init__(self):
        self._age = 0

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, a):
        self._age = a


def main():
    pass

if __name__ == "__main__":
    t = Test()

    if t.age == 0:
        print(t.age)