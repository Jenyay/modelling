from math import sqrt

def equation(a, b, c):
    D = b ** 2 - 4 * a * c
    if D >= 0:
        x1 = (-b + sqrt(D)) / (2 * a)
        x2 = (-b - sqrt(D)) / (2 * a)
        return (x1, x2)
