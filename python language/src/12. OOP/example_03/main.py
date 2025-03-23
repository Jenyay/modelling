from textpost import TextPost

if __name__ == "__main__":
    post = TextPost("Толстой Л.Н.", "Очень длинный текст...")

    print("Автор:", post.author)
    print("Дата:", post.date)
    print("Текст:", post.text)

    post.author = "Чехов А.П."
    print()
    print("Автор:", post.author)
    print("Дата:", post.date)
    print("Текст:", post.text)
