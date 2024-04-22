# src/13. Files/example_13/reader.py
# Чтение данных из файла в двоичном (бинарном) формате

if __name__ == "__main__":
    with open("example.txt", "rb") as file:
        data_bytes = file.read()

    print(f"{type(data_bytes)=}")
    print(f"{data_bytes=}")

    data_str = data_bytes.decode(encoding="utf8")

    print(f"{data_str=}")
