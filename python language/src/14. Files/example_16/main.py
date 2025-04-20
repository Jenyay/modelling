from pathlib import Path
import time

if __name__ == "__main__":
    # Получить текущую рабочую директорию
    workdir = Path.cwd()
    print(f"{workdir=}")

    input("Нажмите Enter для продолжения...\n")

    # Относительный путь до вложенной папки
    foo_rel_path = Path("subdir", "foo")
    print(f"{foo_rel_path=}")

    # Относительный путь до существующего файла
    example_rel_path = Path("subdir", "foo", "example.txt")
    print(f"{example_rel_path=}")

    # Относительный путь до несуществующего файла
    unknown_rel_path = foo_rel_path / "unknown.txt"
    print(f"{unknown_rel_path=}")

    input("Нажмите Enter для продолжения...\n")

    # Получение абсолютных путей до файлов
    example_abs_path = example_rel_path.absolute()
    unknown_abs_path = unknown_rel_path.absolute()

    print(f"{example_abs_path=}")
    print(f"{unknown_abs_path=}")

    input("Нажмите Enter для продолжения...\n")

    # Выделение элементов путей
    print(f"{example_rel_path.parent=}")
    print(f"{example_rel_path.name=}")
    print(f"{foo_rel_path.parent=}")
    print(f"{foo_rel_path.name=}")

    input("Нажмите Enter для продолжения...\n")

    print(f"{example_rel_path.stem=}")
    print(f"{example_rel_path.suffix=}")

    input("Нажмите Enter для продолжения...\n")

    # Проверка существования файлов
    print(f"{foo_rel_path.exists()=}")
    print(f"{example_rel_path.exists()=}")
    print(f"{unknown_rel_path.exists()=}")

    input("Нажмите Enter для продолжения...\n")

    # Проверки, является ли указанный путь файлом или директорией
    print(f"{example_rel_path.is_file()=}")
    print(f"{foo_rel_path.is_file()=}")
    print(f"{unknown_rel_path.is_file()=}")

    input("Нажмите Enter для продолжения...\n")

    print(f"{example_rel_path.is_dir()=}")
    print(f"{foo_rel_path.is_dir()=}")
    print(f"{unknown_rel_path.is_dir()=}")

    input("Нажмите Enter для продолжения...\n")

    # Получение информации о файлах
    file_stat = example_rel_path.stat()

    print(f"{file_stat.st_size=}")

    # Получаем количество секунд, прошедших c 01.01.1970 00:00:00 (UTC)
    # до момента модификации файла
    time_sec = file_stat.st_mtime
    local_time = time.localtime(time_sec)
    print(f"{time_sec=}")
    print(f"{local_time=}")
