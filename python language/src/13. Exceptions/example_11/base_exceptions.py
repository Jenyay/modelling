from math import sqrt

class EquationError(Exception): ...

def equation(a, b, c) -> tuple[float, float]:
    D = b ** 2 - 4 * a * c
    if D < 0:
        raise EquationError("Дискриминант меньше нуля.")
    x1 = (-b + sqrt(D)) / (2 * a)
    x2 = (-b - sqrt(D)) / (2 * a)
    return (x1, x2)

if __name__ == "__main__":
    print("Решение уравнения вида ax^2 + bx + c = 0")
    try:
        input_str = input("Введите a, b и c через пробел: ")
        values = [float(val) for val in input_str.split(" ")]
        result = equation(values[0], values[1], values[2])
        print("Результат вычисления:", result)
    except EquationError as err:
        print("Ошибка решения уравнения.", err)
    except Exception as err:
        print("Ошибка вычисления.", err, type(err))
    except BaseException as err:
        print("\nЧто-то пошло не так.", type(err))
