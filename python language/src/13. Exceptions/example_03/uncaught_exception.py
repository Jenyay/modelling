from math import sqrt

def equation(a, b, c) -> tuple[float, float]:
    D = b ** 2 - 4 * a * c
    if D < 0:
        raise ValueError("Дискриминант меньше нуля.")
    x1 = (-b + sqrt(D)) / (2 * a)
    x2 = (-b - sqrt(D)) / (2 * a)
    return (x1, x2)

def func_1(a, b, c) -> float:
    result = func_2(a, b, c)
    return result[0] + result[1]

def func_2(a, b, c) -> tuple[float, float]:
    result = func_3(a, b, c)
    return (result[0] * 2, result[1] * 2)

def func_3(a, b, c) -> tuple[float, float]:
    result = equation(a, b, c)
    return (result[0] + 1, result[1] + 2)

if __name__ == "__main__":
    a = 1
    b = 2
    c = 10
    result = func_1(a, b, c)
    print("Результат равен", result)
