# Построение трехмерной поверхности для функции вида z = f(x, y)

import matplotlib.pyplot as plt
import numpy as np


def makeData ():
    # Строим сетку в интервале от -10 до 10, имеющую 100 отсчетов по обеим координатам
    x = np.linspace (-10, 10, 100)
    y = np.linspace (-10, 10, 100)

    # Создаем двумерную матрицу-сетку
    xgrid, ygrid = np.meshgrid(x, y)

    # В узлах рассчитываем значение функции
    z = np.sin(xgrid) * np.sin(ygrid) / (xgrid * ygrid)
    return xgrid, ygrid, z


if __name__ == '__main__':
    x, y, z = makeData()

    fig = plt.figure()
    axes = fig.add_subplot(projection='3d')

    axes.plot_surface(x, y, z,
                      color="yellow", edgecolor="black", linewidth=0.5)

    # axes.plot_surface(x, y, z,
    #                   color="white", edgecolor="black", linewidth=0.5,
    #                   shade=False)

    # axes.plot_surface(x, y, z,
    #                   color="white", edgecolor="black", linewidth=0.5,
    #                   rcount=20, ccount=20,
    #                   shade=False)

    # axes.plot_surface(x, y, z,
    #                   cmap="hsv", edgecolor="black", linewidth=0.5)

    plt.show()
