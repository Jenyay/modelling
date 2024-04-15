"""example_01/main.py

Демонстрация создания экземпляра (instance) класса.
"""

from post import Post

if __name__ == "__main__":
    post = Post("Толстой Л.Н.", "Очень длинный текст...")
    post.save()

    print()
    print(f"{type(post)=}")
    print(dir(post))
    print()

    print(post.format())
