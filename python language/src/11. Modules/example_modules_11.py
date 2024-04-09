# example_modules_11.py

from package_02 import add, add_abs, mul 

def spam(a, b, action):
    return action(a, b) * 2 + 1

if __name__ == "__main__":
    foo = spam(2, 3, add)
    bar = spam(2, 3, mul)
    baz = spam(2, -5, add_abs)

    print(f"{foo=}")
    print(f"{bar=}")
    print(f"{baz=}")
