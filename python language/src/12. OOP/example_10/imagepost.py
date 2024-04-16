# example_10/imagepost.py

from datetime import datetime

from basepost import BasePost


class ImagePost(BasePost):
    """Класс поста с картинкой для блога"""

    def __init__(self, author: str, image: str):
        super().__init__(author)
        self._image = image

    def save(self) -> None:
        print("Пост с картинкой сохранен")

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
