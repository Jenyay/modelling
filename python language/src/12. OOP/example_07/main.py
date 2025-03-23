from textpost import TextPost
from imagepost import ImagePost

post1 = TextPost("Толстой Л.Н.", "Очень длинный текст...")
post2 = ImagePost("Малевич К.С.", "black_square.jpg")

print(post1.format())
print()
print(post2.format())
