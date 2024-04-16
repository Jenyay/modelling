"""example_09/main.py

Демонстрация полиморфизма с использованием наследования.
"""

from textpost import TextPost
from imagepost import ImagePost

if __name__ == "__main__":
    post_1 = TextPost("Толстой Л.Н.", "Очень длинный текст...")
    post_1.save()

    post_2 = ImagePost("Малевич К.С.", "https://malevich.ru/black.jpg")
    post_2.save()

    print(dir(post_1))
    print()

    print(dir(post_2))
    print()

    feed = [post_1, post_2]
    for post in feed:
        print(post.format())
        print()
