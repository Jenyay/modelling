from textpost import TextPost

if __name__ == "__main__":
    post = TextPost("Толстой Л.Н.", "Очень длинный текст...")

    print("Автор:", post.author)
    print("Дата:", post.date)

    print("Изменяем текст поста")
    post.text = "Еще более длинный текст..."
