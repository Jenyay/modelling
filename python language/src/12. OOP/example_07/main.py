"""example_07/main.py

Демонстрация использования статического метода класса.
"""

from post import Post

if __name__ == "__main__":
    print("База данных для сохранения постов:", Post.get_database_name())

    post = Post("Толстой Л.Н.", "Очень длинный текст...")
    post.save()
