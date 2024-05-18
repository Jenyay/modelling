# Меняем стиль линий графиков

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

    # Меняем стиль линий графиков
    plt.plot(xdata, ydata1, "-k", label="data 1")
    plt.plot(xdata, ydata2, "--b", label="data 2")
    plt.legend()

    plt.grid()
    plt.show()
