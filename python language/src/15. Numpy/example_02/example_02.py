# Пример расчета функции на сетке с использованием Numpy
import numpy as np

def func(x):
    return np.sin(x) * np.cos(3 * x)

minval = 0
maxval = 10
count = 101

xdata = np.linspace(minval, maxval, count)
ydata = func(xdata)

print(f"{type(xdata)=}")
print(f"{xdata=}")
print(f"{type(ydata)=}")
print(f"{ydata=}")
