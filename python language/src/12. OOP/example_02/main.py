from textpost import TextPost

if __name__ == "__main__":
    post = TextPost("Толстой Л.Н.", "Очень длинный текст...")

    print(dir(post))

    # Не рекомендуемый способ добавления полей класса
    post.title = "Война и мир"
    print()
    print(dir(post))
