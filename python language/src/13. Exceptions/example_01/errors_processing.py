from math import sqrt

def func_1(a, b, c) -> float | None:
    result = func_2(a, b, c)
    return result[0] + result[1] if result is not None else None

def func_2(a, b, c) -> tuple[float, float] | None:
    result = func_3(a, b, c)
    return (result[0] * 2, result[1] * 2) if result is not None else None

def func_3(a, b, c) -> tuple[float, float] | None:
    result = equation(a, b, c)
    return (result[0] + 1, result[1] + 2) if result is not None else None

def equation(a, b, c) -> tuple[float, float] | None:
    D = b ** 2 - 4 * a * c
    if D >= 0:
        x1 = (-b + sqrt(D)) / (2 * a)
        x2 = (-b - sqrt(D)) / (2 * a)
        return (x1, x2)

    return None

if __name__ == "__main__":
    a = 1
    b = 2
    c = 10
    result = func_1(a, b, c)
    if result is None:
        print("Ошибка вычисления.")
    else:
        print("Результат равен", result)
