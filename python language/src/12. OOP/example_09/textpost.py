# example_09/textpost.py

from datetime import datetime


class TextPost:
    """Класс текстового поста для блога"""

    def __init__(self, author: str, text: str):
        self._author = author
        self._text = text
        self._date = datetime.utcnow()

    def save(self) -> None:
        print("Текстовый пост сохранен")

    @property
    def author(self) -> str:
        return self._author

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self._date = datetime.utcnow()

    def format(self) -> str:
        return f"""====
Автор: {self._author}
Дата: {self._date}
----
{self._text}
===="""
