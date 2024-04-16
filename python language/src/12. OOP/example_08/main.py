"""example_08/main.py

Демонстрация полиморфизма без использования наследования классов.
"""

from textpost import TextPost
from imagepost import ImagePost

if __name__ == "__main__":
    post_1 = TextPost("Толстой Л.Н.", "Очень длинный текст...")
    post_1.save()

    post_2 = ImagePost("Малевич К.С.", "https://malevich.ru/black.jpg")
    post_2.save()

    feed = [post_1, post_2]
    for post in feed:
        print(post.format())
        print()
