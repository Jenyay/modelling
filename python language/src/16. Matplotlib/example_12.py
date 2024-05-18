# Явный способ создания объектов Matplotlib

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

    fig = plt.figure(figsize=(10, 5))
    print(f"{type(fig)=}")
    fig.canvas.manager.set_window_title("График функции")

    axes = fig.add_subplot(1, 1, 1)
    print(f"{type(axes)=}")

    curves = axes.plot(xdata, ydata1, "-k", xdata, ydata2, "--b")
    print(f"{curves=}")

    legend = axes.legend(["data 1", "data 2"])
    print(f"{type(legend)=}")

    axes.grid()
    axes.set_xlim(-30, 30)
    axes.set_ylim(-1.0, 2.0)

    xlabel = axes.set_xlabel("X")
    ylabel = axes.set_ylabel("Y")
    title = axes.set_title("y = sin(x) / x")
    print(f"{xlabel=}")
    print(f"{ylabel=}")
    print(f"{title=}")

    plt.show()
