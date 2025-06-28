# coding: utf-8
'''
Построение графика зависимости коэффициента отражения от границы раздела
свободное пространство-диэлектрик от количества ячеек на длину волны
при различных значениях числа Куранта.
'''

import numpy as np
import matplotlib.pyplot as plt


def get_phase(Sc, Nl, eps, mu):
    '''
    Расчет отношения фазовых скоростей в дискретном и непрерывном пространствах.

    Sc - число Куранта.
    Nl - количество ячеек на длину волны.
    eps, mu - проницаемости среды.
    '''
    return np.arcsin(np.sqrt(eps * mu) * np.sin(np.pi * Sc / Nl) / Sc)


if __name__ == '__main__':
    # Количество ячеек на длину волны
    Nl = np.arange(10, 80, 1)
    eps1 = 1
    mu1 = 1

    eps2 = 4
    mu2 = 1

    plt.figure()

    # В цикле меняется число Куранта
    for Sc in np.arange(1, 0, -0.25):
        legend_str = 'Sc = {:.2f}'.format(Sc)

        phase1 = get_phase(Sc, Nl, eps1, mu1)
        phase2 = get_phase(Sc, Nl, eps2, mu2)

        ref_fdtd = ((np.sqrt(eps1) * np.cos(phase2) - np.sqrt(eps2) * np.cos(phase1)) /
                    (np.sqrt(eps1) * np.cos(phase2) + np.sqrt(eps2) * np.cos(phase1)))

        plt.plot(Nl, ref_fdtd, label=legend_str)

    # Аналитический расчет коэффициента отражения
    ref_anal = (np.ones(len(Nl)) *
                (np.sqrt(eps1) - np.sqrt(eps2)) / (np.sqrt(eps1) + np.sqrt(eps2)))
    plt.plot(Nl, ref_anal, '--k', label='Аналитика')

    plt.legend()
    plt.grid()
    plt.xlabel('$N_\lambda$', fontsize=14)
    plt.ylabel('Г', rotation=0, fontsize=14, labelpad=10)

    plt.show()
