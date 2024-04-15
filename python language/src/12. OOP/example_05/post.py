# example_05/post.py

from datetime import datetime


class Post:
    """Класс текстового поста для блога"""

    # Переменная на уровне класса, а не экземпляра класса
    _DATABASE_NAME = "db_posts"

    def __init__(self, author: str, text: str):
        self._author = author
        self._text = text
        self._date = datetime.utcnow()

    def save(self) -> None:
        print(f"Пост сохранен в базу данных {Post._DATABASE_NAME}")

        # Следующая запись также корректна
        # print(f"Пост сохранен в базу данных {self._DATABASE_NAME}")

    def get_author(self) -> str:
        return self._author

    def get_text(self) -> str:
        return self._text

    def set_text(self, text: str) -> None:
        self._text = text
        self._date = datetime.utcnow()

    def format(self) -> str:
        return f"""====
Автор: {self._author}
Дата: {self._date}
----
{self._text}
===="""
