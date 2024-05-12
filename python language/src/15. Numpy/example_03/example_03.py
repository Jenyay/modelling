# Выделение срезов для одномерных массивов
import numpy as np

# Создаем массив и выделяем его срез
foo_ndarray = np.arange(0, 10)
slice_ndarray = foo_ndarray[3: 7]

# Создаем список и выделяем его срез
foo_list = list(range(0, 10))
slice_list = foo_list[3: 7]

print("Первоначальное состояние")
print(f"{foo_ndarray=}")
print(f"{slice_ndarray=}")
print(f"{foo_list=}")
print(f"{slice_list=}")
print()

# Изменяем элементы в срезе массива и списка
slice_ndarray[:] = 100
slice_list[:] = [100] * len(slice_list)

print("После изменения элементов среза")
print(f"{foo_ndarray=}")
print(f"{slice_ndarray=}")
print(f"{foo_list=}")
print(f"{slice_list=}")
