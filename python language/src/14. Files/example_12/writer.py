# src/13. Files/example_12/writer.py
# Ошибка указания неправильной кодировки файла при записи

if __name__ == "__main__":
    lines = ["Hello, world!\n", "Привет, мир!\n", "你好世界!\n"]

    with open("example.txt", "wt", encoding="cp1251") as file:
        file.writelines(lines)
