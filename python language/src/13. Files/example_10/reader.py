# src/13. Files/example_10/reader.py
# Указание кодировки текстового файла

if __name__ == "__main__":
    with open("example.txt", "rt", encoding="cp1251") as file:
        lines = file.readlines()

    print(f"{lines=}")
