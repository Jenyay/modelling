# src/13. Files/example_06/main.py
# Демонстрация порционного чтения текстового файла

if __name__ == "__main__":
    file = open("example.txt", "rt")

    # Будем читать файл последовательно по 8 символов
    buffer_size = 8

    while (text := file.read(buffer_size)) != "":
        print(text, end="|")

    file.close()
