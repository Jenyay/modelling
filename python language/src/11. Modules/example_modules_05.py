# example_modules_05.py

print("Main script - 1")

import tools_debug

print("Main script - 2")

def spam(a, b, action):
    return action(a, b) * 2 + 1

foo = spam(2, 3, tools_debug.add)
bar = spam(2, 3, tools_debug.mul)
baz = spam(2, -5, tools_debug.add_abs)

print(f"{foo=}")
print(f"{bar=}")
print(f"{baz=}")
