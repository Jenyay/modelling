# example_modules_08.py

import tools

def spam(a, b, action):
    return action(a, b) * 2 + 1

if __name__ == "__main__":
    foo = spam(2, 3, tools.add)
    bar = spam(2, 3, tools.mul)
    baz = spam(2, -5, tools.add_abs)

    print(f"{foo=}")
    print(f"{bar=}")
    print(f"{baz=}")
