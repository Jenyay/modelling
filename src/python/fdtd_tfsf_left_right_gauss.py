# -*- coding: utf-8 -*-
'''
Метод полного поля / рассеянного поля (TF / SF).
Гауссов импульс.
Две границы TF / SF.
'''

import numpy as np

import tools


class GaussianPlaneWave:
    ''' Класс с уравнением плоской волны для гауссова сигнала в дискретном виде
    d - определяет задержку сигнала.
    w - определяет ширину сигнала.
    Sc - число Куранта.
    eps - относительная диэлектрическая проницаемость среды, в которой расположен источник.
    mu - относительная магнитная проницаемость среды, в которой расположен источник.
    '''

    def __init__(self, d, w, Sc=1.0, eps=1.0, mu=1.0):
        self.d = d
        self.w = w
        self.Sc = Sc
        self.eps = eps
        self.mu = mu

    def getE(self, m, q):
        '''
        Расчет поля E в дискретной точке пространства m
        в дискретный момент времени q
        '''
        return np.exp(-(((q - m * np.sqrt(self.eps * self.mu) / self.Sc) - self.d) / self.w) ** 2)


if __name__ == '__main__':
    # Характеристическое сопротивление свободного пространства
    Z0 = 120.0 * np.pi

    # Число Куранта
    Sc = 1.0

    # Время расчета в отсчетах
    maxTime = 500

    # Размер области моделирования в отсчетах
    maxSize = 200

    # Левая граница TF/SF
    tfsf_left = 50

    # Правая граница TF/SF
    tfsf_right = 150

    # Датчики для регистрации поля
    probesPos = [75]
    probes = [tools.Probe(pos, maxTime) for pos in probesPos]

    Ez = np.zeros(maxSize)
    Hy = np.zeros(maxSize - 1)

    eps = np.ones(maxSize)
    # eps = np.ones(maxSize) * 4
    mu = np.ones(maxSize - 1)

    source = GaussianPlaneWave(30.0, 10.0, Sc, eps=eps[tfsf_left], mu=mu[tfsf_left])

    # Параметры отображения поля E
    display_field = Ez
    display_ylabel = 'Ez, В/м'
    display_ymin = -1.1
    display_ymax = 1.1

    # Создание экземпляра класса для отображения
    # распределения поля в пространстве
    display = tools.AnimateFieldDisplay(maxSize,
                                        display_ymin, display_ymax,
                                        display_ylabel)

    display.activate()
    display.drawProbes(probesPos)
    display.drawSources([tfsf_left, tfsf_right])

    for q in range(maxTime):
        # Расчет компоненты поля H
        Hy[:] = Hy + (Ez[1:] - Ez[:-1]) * Sc / (Z0 * mu)

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Hy[tfsf_left - 1] -= (Sc / (Z0 * mu[tfsf_left - 1])) * source.getE(tfsf_left, q)
        Hy[tfsf_right - 1] += (Sc / (Z0 * mu[tfsf_right - 1])) * source.getE(tfsf_right, q)

        # Hy[tfsf_left - 1] -= (Sc / (Z0 * mu[tfsf_left - 1])) * source.getE(0, q)
        # Hy[tfsf_right - 1] += (Sc / (Z0 * mu[tfsf_right - 1])) * source.getE(tfsf_right - tfsf_left, q)

        # Граничные условия для поля E
        Ez[0] = Ez[1]
        Ez[-1] = Ez[-2]

        # Расчет компоненты поля E
        Ez[1:-1] = Ez[1: -1] + (Hy[1:] - Hy[: -1]) * Sc * Z0 / eps[1: -1]

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Ez[tfsf_left] += (Sc / (np.sqrt(eps[tfsf_left] * mu[tfsf_left]))) * source.getE(tfsf_left - 0.5, q + 0.5)
        Ez[tfsf_right] -= (Sc / (np.sqrt(eps[tfsf_right] * mu[tfsf_right]))) * source.getE(tfsf_right - 0.5, q + 0.5)

        # Ez[tfsf_left] += (Sc / (np.sqrt(eps[tfsf_left] * mu[tfsf_left]))) * source.getE(-0.5, q + 0.5)
        # Ez[tfsf_right] -= (Sc / (np.sqrt(eps[tfsf_right] * mu[tfsf_right]))) * source.getE(tfsf_right - tfsf_left - 0.5, q + 0.5)

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(display_field, q)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    tools.showProbeSignals(probes, -1.1, 1.1)
