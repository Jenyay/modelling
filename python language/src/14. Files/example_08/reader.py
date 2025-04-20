# src/13. Files/example_08/reader.py
# Демонстрация одновременного открытия файла разными скриптами

if __name__ == "__main__":
    file = open("example.txt", "rt")

    lines = file.readlines()
    print(f"{lines=}")

    input("Нажмите Enter...")

    file.close()
