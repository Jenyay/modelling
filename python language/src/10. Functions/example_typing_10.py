from collections.abc import Iterable

def spam(foo: Iterable[int]) -> dict[int, bool]:
    return {n: n % 2 == 0 for n in foo}

foo = spam({10, 11, 12, 14, 17})
print(f"{foo=}")
