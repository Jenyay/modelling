from datetime import datetime, timezone

class TextPost:
    """Класс текстового поста для блога"""

    def __init__(self, author, text):
        print(f"TextPost.__init__(). self: {self}")
        self.author = author
        self.text = text
        self.date = datetime.now(timezone.utc)
