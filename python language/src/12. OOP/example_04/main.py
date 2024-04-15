"""example_04/main.py

Демонстрация переменных уровня класса (статические переменные).
"""

from post import Post

if __name__ == "__main__":
    post = Post("Толстой Л.Н.", "Очень длинный текст...")
    post.save()

    print()
    print(dir(Post))

    print()
    print(dir(post))
