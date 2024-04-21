"""example_16/main.py

Демонстрация применения функции len к созданным классам
"""

from textpost import TextPost
from imagepost import ImagePost

if __name__ == "__main__":
    text_post = TextPost("Толстой Л.Н.", "Очень длинный текст...")
    text_post.save()

    image_post = ImagePost("Малевич К.С.", "https://malevich.ru/black.jpg")
    image_post.save()

    print("Размер контента текстового поста:", len(text_post))
    print("Размер контента поста с картинкой:", len(image_post))
