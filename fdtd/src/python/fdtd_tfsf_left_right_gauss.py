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
    # Волновое сопротивление свободного пространства
    W0 = 120.0 * np.pi

    # Число Куранта
    Sc = 1.0

    # Время расчета в отсчетах
    maxTime = 400

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
    Hy = np.zeros(maxSize)

    source = GaussianPlaneWave(30.0, 10.0, Sc)

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
        # Граничные условия для поля H
        Hy[-1] = Hy[-2]

        # Расчет компоненты поля H
        Ez_shift = Ez[1:]
        Hy[:-1] = Hy[:-1] + (Ez_shift - Ez[:-1]) * Sc / W0

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Hy[tfsf_left - 1] -= (Sc / W0) * source.getE(tfsf_left, q)
        Hy[tfsf_right - 1] += (Sc / W0) * source.getE(tfsf_right, q)

        # Hy[tfsf_left - 1] -= (Sc / W0) * source.getE(0, q)
        # Hy[tfsf_right - 1] += (Sc / W0) * source.getE(tfsf_right - tfsf_left, q)

        # Граничные условия для поля E
        Ez[0] = Ez[1]

        # Расчет компоненты поля E
        Hy_shift = Hy[:-1]
        Ez[1:] = Ez[1:] + (Hy[1:] - Hy_shift) * Sc * W0

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Ez[tfsf_left] += Sc * source.getE(tfsf_left - 0.5, q + 0.5)
        Ez[tfsf_right] -= Sc * source.getE(tfsf_right - 0.5, q + 0.5)

        # Ez[tfsf_left] += Sc * source.getE(-0.5, q + 0.5)
        # Ez[tfsf_right] -= Sc * source.getE(tfsf_right - tfsf_left - 0.5, q + 0.5)

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(display_field, q)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    tools.showProbeSignals(probes, -1.1, 1.1)
