# example_08/imagepost.py

from datetime import datetime


class ImagePost:
    """Класс поста с картинкой для блога"""

    def __init__(self, author: str, image: str):
        self._author = author
        self._image = image
        self._date = datetime.utcnow()

    def save(self) -> None:
        print("Пост с картинкой сохранен")

    @property
    def author(self) -> str:
        return self._author

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, image: str) -> None:
        self._image = image
        self._date = datetime.utcnow()

    def format(self) -> str:
        return f"""====
Автор: {self._author}
Дата: {self._date}
Картинка: {self._image}
===="""
