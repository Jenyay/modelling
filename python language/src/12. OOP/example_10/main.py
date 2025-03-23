from textpost import TextPost
from imagepost import ImagePost

feed = []
feed.append(TextPost("Толстой Л.Н.", "Очень длинный текст..."))
feed.append(ImagePost("Малевич К.С.", "black_square.jpg"))

for post in feed:
    print(post.format())
