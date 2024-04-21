import math

class MathAction:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __call__(self, a, b) -> float:
        print("MathAction.__call__()")
        return a * math.sin(self.x) + b * math.cos(self.y)


def add(a, b):
    return a + b

def spam(a, b, action):
    return action(a, b) * 2 + 1

foo = spam(2, 3, add)
bar = spam(2, 3, MathAction(math.pi / 3, math.pi / 4))

print(f"{foo=}")
print(f"{bar=}")
