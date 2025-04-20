import os
import os.path
import time

if __name__ == "__main__":
    # Получить текущую рабочую директорию
    workdir = os.getcwd()
    print(f"{workdir=}")

    # Путь до выполняемого текущего модуля
    print(f"{__file__=}")

    input("Нажмите Enter для продолжения...\n")

    # Относительный путь до вложенной папки
    foo_rel_path = os.path.join("subdir", "foo")
    print(f"{foo_rel_path=}")

    # Относительный путь до существующего файла
    example_rel_path = os.path.join("subdir", "foo", "example.txt")
    print(f"{example_rel_path=}")

    # Относительный путь до несуществующего файла
    unknown_rel_path = os.path.join("subdir", "foo", "unknown.txt")
    print(f"{unknown_rel_path=}")

    input("Нажмите Enter для продолжения...\n")

    # Получение абсолютных путей до файлов
    example_abs_path = os.path.abspath(example_rel_path)
    unknown_abs_path = os.path.abspath(unknown_rel_path)

    print(f"{example_abs_path=}")
    print(f"{unknown_abs_path=}")

    input("Нажмите Enter для продолжения...\n")

    # Выделение элементов путей
    print(f"{os.path.dirname(example_rel_path)=}")
    print(f"{os.path.basename(example_rel_path)=}")
    print(f"{os.path.dirname(foo_rel_path)=}")
    print(f"{os.path.basename(foo_rel_path)=}")

    input("Нажмите Enter для продолжения...\n")

    print(f"{os.path.split(example_rel_path)=}")
    print(f"{os.path.split(foo_rel_path)=}")

    input("Нажмите Enter для продолжения...\n")

    print(f"{os.path.splitext(example_rel_path)=}")
    print(f"{os.path.splitext(foo_rel_path)=}")

    input("Нажмите Enter для продолжения...\n")

    # Проверка существования файлов
    print(f"{os.path.exists(foo_rel_path)=}")
    print(f"{os.path.exists(example_rel_path)=}")
    print(f"{os.path.exists(unknown_rel_path)=}")

    input("Нажмите Enter для продолжения...\n")

    # Проверки, является ли указанный путь файлом или директорией
    print(f"{os.path.isfile(example_rel_path)=}")
    print(f"{os.path.isfile(foo_rel_path)=}")
    print(f"{os.path.isfile(unknown_rel_path)=}")

    input("Нажмите Enter для продолжения...\n")

    print(f"{os.path.isdir(example_rel_path)=}")
    print(f"{os.path.isdir(foo_rel_path)=}")
    print(f"{os.path.isdir(unknown_rel_path)=}")

    input("Нажмите Enter для продолжения...\n")

    # Получение информации о файлах
    print(f"{os.path.getsize(example_rel_path)=}")

    # Получаем количество секунд, прошедших c 01.01.1970 00:00:00 (UTC)
    # до момента модификации файла
    time_sec = os.path.getmtime(example_rel_path)
    local_time = time.localtime(time_sec)
    print(f"{time_sec=}")
    print(f"{local_time=}")
