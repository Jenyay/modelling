# example_01/post.py

from datetime import datetime

class Post:
    def __init__(self, author: str, text: str):
        self._author = author
        self._text = text
        self._date = datetime.utcnow()

    def save(self) -> None:
        print("Пост сохранен")

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
