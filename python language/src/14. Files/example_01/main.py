# src/13. Files/example_01/main.py

if __name__ == "__main__":
    file = open("example.txt", "wt")

    print(type(file))
    print(dir(file))

    file.close()
