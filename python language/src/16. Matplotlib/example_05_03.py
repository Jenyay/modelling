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

    plt.plot(xdata, ydata, linestyle="-.", color="g")
    # plt.plot(xdata, ydata, linestyle="-.", color="green")
    # plt.plot(xdata, ydata, linestyle="-.", color="goldenrod")
    # plt.plot(xdata, ydata, linestyle="-.", color="xkcd:moss green")
    # plt.plot(xdata, ydata, linestyle="-.", color="#31D115")
    # plt.plot(xdata, ydata, linestyle="-.", color="#A25")
    # plt.plot(xdata, ydata, linestyle="-.", color=(0.5, 0.2, 0.7))
    # plt.plot(xdata, ydata, linestyle="-.", color="0.6")

    plt.grid()
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.show()
