def func():
    try:
        print("Вошли в блок try.")
        return
        print("Выходим из блока try.")
    except ValueError:
        print("Вошли в блок except.")
    else:
        print("Вошли в блок else.")
    finally:
        print("Вошли в блок finally.")

if __name__ == "__main__":
    print("Вызов функции func()")
    func()
    print("Вышли из функции func()") 
