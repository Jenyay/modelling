from random import randrange

def raise_error():
    if randrange(2) == 0:
        raise ZeroDivisionError("Делить на ноль нельзя.")
    raise ValueError("Неправильное значение.")

if __name__ == "__main__":
    try:
        raise_error()
    except ZeroDivisionError as err:
        print("ZeroDivisionError.", err)
    except ValueError as err:
        print("ValueError.", err)

    print("После обработки исключения.")
