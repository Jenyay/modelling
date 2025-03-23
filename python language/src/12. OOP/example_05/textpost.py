from datetime import datetime, timezone

class TextPost:
    """Класс текстового поста для блога"""

    def __init__(self, author, text):
        self._author = author
        self._text = text
        self._date = datetime.now(timezone.utc)
        self._save()

    def _save(self):
        print("Пост сохранен.")

    def get_author(self): return self._author

    def get_text(self): return self._text

    def set_text(self, value):
        self._text = value
        self._save()

    def get_date(self): return self._date
