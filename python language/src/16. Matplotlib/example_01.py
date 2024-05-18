# Импортируем один из пакетов Matplotlib
import matplotlib.pyplot as plt
import numpy as np


# Будем рисовать график этой функции
def func(x):
    """
    sinc(x)
    """
    return np.sin(x) / x if x != 0 else 1.0


if __name__ == "__main__":
    # Интервал изменения переменной по оси X
    xmin = -20.0
    xmax = 20.0

    # Количество отсчетов на заданном интервале
    count = 200

    # Создадим список координат по оси X на отрезке [-xmin; xmax], включая концы
    xdata = np.linspace(xmin, xmax, count)

    # Вычислим значение функции в заданных точках
    ydata = [func(x) for x in xdata]

    # Нарисуем одномерный график
    plt.plot(xdata, ydata)

    # Покажем окно с нарисованным графиком
    plt.show()
