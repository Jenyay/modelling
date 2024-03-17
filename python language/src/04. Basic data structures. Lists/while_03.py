while True:
    name = input("Введите имя: ")
    # if not name:
    if name == "":
        break
    elif name == "...":
        continue

    print("Привет,", name)
