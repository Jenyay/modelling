# Создание копии массивов
import numpy as np

foo = np.arange(0, 10)
foo_slice = foo[:]
foo_copy = foo.copy()

print("Первоначальное состояние")
print(f"{foo=}")
print(f"{foo_slice=}")
print(f"{foo_copy=}")
print()

foo_copy[5:] = 0

print("После изменения элементов копии")
print(f"{foo=}")
print(f"{foo_copy=}")
print()

foo_slice[5:] = 0

print("После изменения элементов среза")
print(f"{foo=}")
print(f"{foo_slice=}")
