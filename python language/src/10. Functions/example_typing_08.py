from typing import Dict, List


def spam(foo: List[int]) -> Dict[int, bool]:
    return {n: n % 2 == 0 for n in foo}

foo = spam([10, 11, 12, 14, 17])
print(f"{foo=}")
