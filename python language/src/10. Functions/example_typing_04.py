from typing import Union

# В качестве первого параметра у функции
# ожидается строка или целое число.
# Функция может вернуть строку или целое число
def mul(a: Union[str, int], b: int) -> Union[str, int]:
    return a * b

foo = mul(10, 3)
bar = mul("spam", 3)

print(f"{foo=}")
print(f"{bar=}")
