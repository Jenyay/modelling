# example_01/example_01.py

from post import Post

if __name__ == "__main__":
    post = Post("Толстой Л.Н.", "Очень длинный текст...")
    post.save()

    print(f"{type(post)=}")
    print(post.format())
