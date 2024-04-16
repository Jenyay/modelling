# example_10/textpost.py

from datetime import datetime

from basepost import BasePost


class TextPost(BasePost):
    """Класс текстового поста для блога"""

    def __init__(self, author: str, text: str):
        super().__init__(author)
        self._text = text

    def save(self) -> None:
        print("Текстовый пост сохранен")

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
