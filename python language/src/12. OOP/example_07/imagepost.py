from datetime import datetime, timezone

class ImagePost:
    """Класс поста с картинкой для блога"""

    def __init__(self, author, image):
        self._author = author
        self._image = image
        self._date = datetime.now(timezone.utc)
        self._save()

    def _save(self):
        print("Пост с картинкой сохранен.")

    @property
    def author(self): return self._author

    @property
    def image(self): return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self._save()

    @property
    def date(self): return self._date

    def format(self):
        return f"""====
Автор: {self._author}
Дата: {self._date}
Картинка: {self._image}
===="""
