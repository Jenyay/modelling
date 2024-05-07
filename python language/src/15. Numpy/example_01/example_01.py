# Пример расчета функции на сетке без использования Numpy
from array import array
import math

def func(x):
    return math.sin(x) * math.cos(3 * x)

minval = 0
maxval = 10
count = 101
step = (maxval - minval) / (count - 1)

xdata = array('d', [0] * count)
ydata = array('d', [0] * count)

for n in range(count):
    xdata[n] = minval + n * step
    ydata[n] = func(xdata[n])

print(f"{xdata=}")
print(f"{ydata=}")
