from basepost import BasePost

class ImagePost(BasePost):
    """Класс поста с картинкой для блога"""

    def __init__(self, author, image):
        print("TextPost.__init__()")
        super().__init__(author)
        self._image = image
        self._save()

    def _save(self):
        print("Пост с картинкой сохранен.")

    @property
    def image(self): return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self._save()
