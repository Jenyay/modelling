# src/13. Files/example_04/main.py
# Демонстрация чтения текстового файла в виде списка строк

if __name__ == "__main__":
    file = open("example.txt", "rt")

    data = file.readlines()
    print(f"{data=}")

    file.close()
