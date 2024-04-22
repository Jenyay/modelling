# src/13. Files/example_13/writer.py
# Запись данных в файл в двоичном (бинарном) формате

if __name__ == "__main__":
    data_str = "\n".join(["Hello, world!", "Привет, мир!", "你好世界!"])
    data_bytes = data_str.encode(encoding="utf8")

    print(f"{type(data_bytes)=}")
    print(f"{data_bytes=}")

    with open("example.txt", "wb") as file:
        file.write(data_bytes)
