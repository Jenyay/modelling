# Рисование нескольких графиков в одном окне
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
    ydata3 = [func(x * 2) for x in xdata]

    # Рисование нескольких графиков в одном окне
    plt.subplot(2, 2, 1)
    plt.plot(xdata, ydata1, label="data 1")
    plt.legend()
    plt.grid()

    plt.subplot(2, 2, 2)
    plt.plot(xdata, ydata2, label="data 2")
    plt.legend()
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(xdata, ydata3, label="data 3")
    plt.legend()
    plt.grid()

    plt.show()
