# example_modules_04.py

# Не рекомендуемый способ импорта!
from tools import *

def spam(a, b, action):
    return action(a, b) * 2 + 1

foo = spam(2, 3, add)
bar = spam(2, 3, mul)
baz = spam(2, -5, add_abs)

print(f"{foo=}")
print(f"{bar=}")
print(f"{baz=}")
