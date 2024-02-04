# -*- coding: utf-8 -*-
'''
Моделирование распространения ЭМ волны, падающей на границу
вакуум - диэлектрик с потерями.
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
    maxTime = 600

    # Размер области моделирования в отсчетах
    maxSize = 200

    # Положение источника в отсчетах
    sourcePos = 50

    # Датчики для регистрации поля
    probesPos = [110, 130, 150, 170]
    probes = [tools.Probe(pos, maxTime) for pos in probesPos]

    # Положение начала диэлектрика с потерями
    layer_x = 100

    # Параметры среды
    # Диэлектрическая проницаемость
    eps = np.ones(maxSize)
    eps[layer_x:] = 9.0

    # Магнитная проницаемость
    mu = np.ones(maxSize - 1)

    # Потери в среде. loss = sigma * dt / (2 * eps * eps0)
    loss = np.zeros(maxSize)
    loss[layer_x:] = 0.01

    ceze = (1.0 - loss) / (1.0 + loss)
    cezh = W0 / (eps * (1.0 + loss))

    Ez = np.zeros(maxSize)
    Hy = np.zeros(maxSize - 1)

    source = GaussianPlaneWave(30.0, 10.0, Sc, eps[sourcePos], mu[sourcePos])

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
    display.drawSources([sourcePos])
    display.drawBoundary(layer_x)

    for q in range(maxTime):
        # Расчет компоненты поля H
        Hy = Hy + (Ez[1:] - Ez[:-1]) * Sc / (W0 * mu)

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Hy[sourcePos - 1] -= Sc / (W0 * mu[sourcePos - 1]) * source.getE(0, q)

        # Граничные условия для поля E
        Ez[0] = Ez[1]

        # Расчет компоненты поля E
        Ez[1:-1] = ceze[1: -1] * Ez[1:-1] + cezh[1: -1] * (Hy[1:] - Hy[:-1])

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Ez[sourcePos] += (Sc / (np.sqrt(eps[sourcePos] * mu[sourcePos])) *
                          source.getE(-0.5, q + 0.5))

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(display_field, q)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    tools.showProbeSignals(probes, -1.1, 1.1)
