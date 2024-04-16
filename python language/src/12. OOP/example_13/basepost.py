# example_13/basepost.py

from abc import ABCMeta, abstractmethod
from datetime import datetime


class BasePost(metaclass=ABCMeta):
    """Базовый класс для постов любого вида"""

    def __init__(self, author: str):
        self._author = author
        self._date = datetime.utcnow()

    @property
    def author(self) -> str:
        return self._author

    @abstractmethod
    def save(self) -> None:
        return

    @abstractmethod
    def format(self) -> str:
        return ""
