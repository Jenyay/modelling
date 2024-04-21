def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def spam(a, b, action):
    return action(a, b) * 2 + 1

foo = spam(2, 3, add)
bar = spam(2, 3, mul)

print(dir(add))
print()

print(f"{foo=}")
print(f"{bar=}")
