# src/13. Files/example_08/writer.py
# Демонстрация одновременного открытия файла разными скриптами

if __name__ == "__main__":
    file = open("example.txt", "wt")

    lines = ["Hello, world!\n" "Привет, мир!\n", "你好世界!\n"]
    file.writelines(lines)

    input("Нажмите Enter...")

    file.close()
