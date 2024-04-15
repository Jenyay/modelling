"""example_06/main.py

Демонстрация использования свойств (properties) класса.
"""

from post import Post

if __name__ == "__main__":
    post = Post("Толстой Л.Н.", "Очень длинный текст...")

    print(f"{post.text=}")
    print(post.format())

    post.text = "Еще более длинный текст"

    print()
    print(f"{post.text=}")
    print(post.format())
