"""example_05/main.py

Демонстрация переменных уровня класса (статические переменные).
"""

from post import Post

if __name__ == "__main__":
    post_1 = Post("Толстой Л.Н.", "Очень длинный текст...")
    post_2 = Post("Чехов А.П.", "Очень краткий текст.")

    post_1.save()
    post_2.save()

    # Не надо так делать!
    Post._DATABASE_NAME = "other_db_posts"

    post_1.save()
    post_2.save()
