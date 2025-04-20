# src/13. Files/example_02/main.py
# Демонстрация записи текстовых данных в файл

if __name__ == "__main__":
    file = open("example.txt", "wt")

    file.write("Hello, ")
    file.write("world!\n")

    lines = ["Привет, мир!\n", "你好世界!\n"]
    file.writelines(lines)

    file.close()
