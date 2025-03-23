from abc import ABCMeta, abstractmethod
from datetime import datetime, timezone

class BasePost(metaclass=ABCMeta):
    """Базовый класс для постов блога"""

    def __init__(self, author):
        print("BasePost.__init__()")
        self._author = author
        self._date = datetime.now(timezone.utc)

    @property
    def author(self): return self._author

    @property
    def date(self): return self._date

    @abstractmethod
    def format(self):
        ...

    @abstractmethod
    def _save(self):
        ...
