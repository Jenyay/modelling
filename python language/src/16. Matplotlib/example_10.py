# Другой способ добавление легенды

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

    # Другой способ добавление легенды
    plt.plot(xdata, ydata1, "-k", xdata, ydata2, "--b")
    plt.legend(["data 1", "data 2"])

    plt.grid()
    plt.show()
