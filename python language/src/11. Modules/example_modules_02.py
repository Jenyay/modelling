# example_modules_02.py

import tools as tl

def spam(a, b, action):
    return action(a, b) * 2 + 1

foo = spam(2, 3, tl.add)
bar = spam(2, 3, tl.mul)
baz = spam(2, -5, tl.add_abs)

print(f"{foo=}")
print(f"{bar=}")
print(f"{baz=}")
