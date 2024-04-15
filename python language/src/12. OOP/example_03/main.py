"""example_03/main.py

Демонстрация не рекомендуемого способа доступа к переменным класса.
"""

from post import Post

if __name__ == "__main__":
    post = Post("Толстой Л.Н.", "Очень длинный текст...")
    post.save()

    print(post.format())

    # Некорректный доступ к внутренним переменным класса
    post._author = "Чехов А.П."
    post._text = "Очень короткий текст"

    print(post.format())
