# Рисование нескольких графиков в одних осях

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
    ydata1 = [func(x) for x in xdata]
    ydata2 = [func(x * 0.2) for x in xdata]

    # Рисование нескольких графиков в одних осях
    plt.plot(xdata, ydata1, xdata, ydata2)

    plt.grid()
    plt.show()
