# src/13. Files/example_09/reader.py
# Демонстрация автоматического закрытия файла с помощью оператора with

if __name__ == "__main__":
    with open("example.txt", "rt") as file:
        lines = file.readlines()

    print(f"{lines=}")
    input("Нажмите Enter...")
