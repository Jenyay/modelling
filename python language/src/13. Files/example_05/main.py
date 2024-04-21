# src/13. Files/example_05/main.py
# Демонстрация построчного чтения текстового файла

if __name__ == "__main__":
    file = open("example.txt", "rt")

    for line in file:
        print(line)

    file.close()
