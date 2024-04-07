import math

def spam(a: float, b: float) -> None | float:
    if a + b >= 0:
        return math.sqrt(a + b)
    return None


foo = spam(4, 5)
bar = spam(-10, 1)

print(f"{foo=}")
print(f"{bar=}")
