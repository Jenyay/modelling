def raise_error():
    try:
        raise ValueError("Неправильное значение.")
    except ValueError:
        print("Обработка исключения внутри raise_error().")
        raise

if __name__ == "__main__":
    try:
        raise_error()
    except ValueError as err:
        print("Обработка исключения в основном скрипте.")
        print(err)

    print("После обработки исключения.")
