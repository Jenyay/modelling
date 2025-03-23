from textpost import TextPost

if __name__ == "__main__":
    post = TextPost("Толстой Л.Н.", "Очень длинный текст...")

    print(f"{type(post)=}")
    print()
    print(dir(post))
    print()
    print("Автор:", post.author)
    print("Дата:", post.date)
