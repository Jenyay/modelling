from basepost import BasePost

class TextPost(BasePost):
    """Класс текстового поста для блога"""

    def __init__(self, author, text):
        print("TextPost.__init__()")
        super().__init__(author)
        self._text = text
        self._save()

    def _save(self):
        print("Текстовый пост сохранен.")

    @property
    def text(self): return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._save()

    def format(self):
        return f"""====
Автор: {self._author}
Дата: {self._date}
----
{self._text}
===="""
