from textpost import TextPost

if __name__ == "__main__":
    post = TextPost("Толстой Л.Н.", "Очень длинный текст...")

    print("Автор:", post._author)
    print("Дата:", post._date)

    print("Изменяем текст поста")
    post._text = "Еще более длинный текст..."
