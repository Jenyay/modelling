# example_modules_01.py

import tools

def spam(a, b, action):
    return action(a, b) * 2 + 1

foo = spam(2, 3, tools.add)
bar = spam(2, 3, tools.mul)
baz = spam(2, -5, tools.add_abs)

print(f"{foo=}")
print(f"{bar=}")
print(f"{baz=}")
