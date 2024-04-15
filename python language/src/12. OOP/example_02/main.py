"""example_02/main.py

Демонстрация добавления переменной класса вне класса.
Так делать не надо.
"""

from post import Post

if __name__ == "__main__":
    post = Post("Толстой Л.Н.", "Очень длинный текст...")

    print()
    print(dir(post))

    # Так лучше не делать
    post.other_value = "Новая переменная в классе"

    print()
    print(dir(post))
