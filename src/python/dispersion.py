# coding: utf-8
'''
Построение графика зависимости отношения фазовых скоростей в дискретном и
непрерывном пространствах в зависимости от количества ячеек на длину волны
при различных значениях числа Куранта.
'''

import numpy as np
import matplotlib.pyplot as plt


def getDispersionRatio(Sc, Nl, eps, mu):
    '''
    Расчет отношения фазовых скоростей в дискретном и непрерывном пространствах.

    Sc - число Куранта.
    Nl - количество ячеек на длину волны.
    eps, mu - проницаемости среды.
    '''
    numerator = np.pi * np.sqrt(eps * mu)
    denominator = Nl * np.arcsin(np.sqrt(eps * mu)
                                 * np.sin(np.pi * Sc / Nl) / Sc)
    return numerator / denominator


if __name__ == '__main__':
    # Количество ячеек на длину волны
    Nl = np.arange(3, 21, 0.1)
    eps = 1
    mu = 1

    plt.figure()

    # В цикле меняется число Куранта
    for Sc in np.arange(1, 0, -0.25):
        legend_str = 'Sc = {:.2f}'.format(Sc)
        ratio = np.abs(getDispersionRatio(Sc, Nl, eps, mu))
        plt.plot(Nl, ratio, label=legend_str)

    plt.legend()
    plt.grid()
    plt.xlabel('$N_\lambda$', fontsize=14)
    plt.ylabel(r'$\frac{\widetilde{c}}{c}$',
               rotation=0, fontsize=14, labelpad=10)
    plt.ylim(0.65, 1.05)

    plt.show()
