class MyException(Exception):
    ...

def raise_error(filename, value):
    raise MyException("Это MyException.", filename, value)

if __name__ == "__main__":
    try:
        raise_error("invalid.txt", 42)
    except MyException as err:
        print("Что-то пошло не так.")
        print(f"Сообщение: {err.args[0]}")
        print(f"Имя файла: {err.args[1]}")
        print(f"Значение: {err.args[2]}")
        print(err)
