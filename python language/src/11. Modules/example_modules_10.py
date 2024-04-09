# example_modules_10.py

from package_01.add import add
from package_01.add_abs import add_abs
from package_01.mul import mul

def spam(a, b, action):
    return action(a, b) * 2 + 1

if __name__ == "__main__":
    foo = spam(2, 3, add)
    bar = spam(2, 3, mul)
    baz = spam(2, -5, add_abs)

    print(f"{foo=}")
    print(f"{bar=}")
    print(f"{baz=}")
