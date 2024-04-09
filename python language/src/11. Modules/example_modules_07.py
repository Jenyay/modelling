# example_modules_07.py

import tools_vars

print(f"example_modules_07.py: {__name__=}")

def spam(a, b, action):
    return action(a, b) * 2 + 1

foo = spam(2, 3, tools_vars.add)
bar = spam(2, 3, tools_vars.mul)
baz = spam(2, -5, tools_vars.add_abs)

print(f"{foo=}")
print(f"{bar=}")
print(f"{baz=}")
