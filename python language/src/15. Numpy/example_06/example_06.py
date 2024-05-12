# Модификация срезов двумерных массивов
import numpy as np

# Создание матрицы из последовательности целых чисел
matrix = np.arange(0, 36).reshape((6, 6))
bar = matrix[1:7:2, 1:7:2]

print("До изменения среза")
print("matrix:")
print(matrix)
print()

print("bar:")
print(bar)
print()

bar[:,:] = 0

print("После изменения среза")
print("matrix:")
print(matrix)
print()

print("bar:")
print(bar)
print()
