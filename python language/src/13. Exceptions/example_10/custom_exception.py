class MyException(Exception):
    def __init__(self, message:str, filename:str, value:int):
        super().__init__(message, filename, value)
        self.message = message
        self.filename = filename
        self.value = value

def raise_error(filename, value):
    raise MyException("Это MyException.", filename, value)

if __name__ == "__main__":
    try:
        raise_error("invalid.txt", 42)
    except MyException as err:
        print("Что-то пошло не так.")
        print(f"Сообщение: {err.message}")
        print(f"Имя файла: {err.filename}")
        print(f"Значение: {err.value}")
        print(err)
