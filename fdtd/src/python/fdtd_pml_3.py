# -*- coding: utf-8 -*-
'''
Моделирование распространения ЭМ волны, падающей на границу
вакуум - диэлектрик с без потерь.
Слева - PEC.
Справа - многослойный поглощающий полностью согласованный слой.
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
    maxTime = 950

    # Размер области моделирования в отсчетах
    maxSize = 200

    # Положение источника в отсчетах
    sourcePos = 110

    # Датчики для регистрации поля
    probesPos = [125]
    probes = [tools.Probe(pos, maxTime) for pos in probesPos]

    # Координаты и потери для поглощающих слоев
    layer_loss_x = [160, 170, 180, 190]
    layer_loss_value = [0.005, 0.010, 0.015, 0.020]

    # Параметры среды
    # Диэлектрическая проницаемость
    eps = np.ones(maxSize)
    eps[:] = 9.0

    # Магнитная проницаемость
    mu = np.ones(maxSize - 1)

    # Потери в среде. loss = sigma * dt / (2 * eps * eps0)
    loss = np.zeros(maxSize)
    for x, value in zip(layer_loss_x, layer_loss_value):
        loss[x:] = value

    # Магнитные потери в среде. loss_m = sigma_m * dt / (2 * mu * mu0)
    loss_m = np.zeros(maxSize - 1)
    loss_m[:] = loss[:-1]

    # Коэффициенты для расчета поля E
    ceze = (1.0 - loss) / (1.0 + loss)
    cezh = (Sc * W0) / (eps * (1.0 + loss))

    # Коэффициенты для расчета поля H
    chyh = (1.0 - loss_m) / (1.0 + loss_m)
    chye = Sc / (mu * W0 * (1.0 + loss_m))

    # Усреднение коэффициентов на границах поглощающего слоя
    for x in layer_loss_x:
        ceze[x] = (ceze[x - 1] + ceze[x + 1]) / 2
        cezh[x] = (cezh[x - 1] + cezh[x + 1]) / 2

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

    for x in layer_loss_x:
        display.drawBoundary(x)

    for q in range(maxTime):
        # Расчет компоненты поля H
        Hy[:] = chyh * Hy + chye * (Ez[1:] - Ez[:-1])

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Hy[sourcePos - 1] -= Sc / (W0 * mu[sourcePos - 1]) * source.getE(0, q)

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
