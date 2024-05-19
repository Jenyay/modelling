# Перегрузка операторов

class Foo:
    def __init__(self, x ,y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Foo: (X = {self.x}; Y = {self.y})"

    def __add__(self, o):
        return Foo(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Foo(self.x - o.x, self.y - o.y)


if __name__ == "__main__":
    bar = Foo(10, 20)
    baz = Foo(5, 6)
    spam = bar + baz
    eggs = bar - baz

    print(f"{type(spam)=}")
    print(spam)
    print(f"{type(eggs)=}")
    print(eggs)
