# Добвляем метки к осям
import matplotlib.pyplot as plt
import numpy as np


def func(x):
    """
    sinc(x)
    """
    return np.sin(x) / x if x != 0 else 1.0


if __name__ == "__main__":
    xmin = -20.0
    xmax = 20.0
    count = 200

    xdata = np.linspace(xmin, xmax, count)
    ydata = [func(x) for x in xdata]

    plt.plot(xdata, ydata)
    plt.grid()
    plt.xlim(-10, 10)
    plt.ylim(-1, 2)

    # Добавляем метки к осям
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()
