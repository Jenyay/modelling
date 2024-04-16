# example_11/basepost.py

from datetime import datetime


class BasePost:
    """Базовый класс для постов любого вида"""

    def __init__(self, author: str):
        self._author = author
        self._date = datetime.utcnow()

    @property
    def author(self) -> str:
        return self._author
