# -*- coding: utf-8 -*-
'''
Моделирование распространения ЭМ волны, падающей на границу
вакуум - идеальный диэлектрик.

Неравномерная сетка (Sc зависит от индекса)
'''

import numpy

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
        return numpy.exp(-(((q - m * numpy.sqrt(self.eps * self.mu) / self.Sc) - self.d) / self.w) ** 2)


if __name__ == '__main__':
    # Волновое сопротивление свободного пространства
    W0 = 120.0 * numpy.pi

    # Время расчета в отсчетах
    maxTime = 800

    # Размер области моделирования в отсчетах
    maxSize = 600

    # Положение источника в отсчетах
    sourcePos = 50

    # Датчики для регистрации поля
    probesPos = [75, 400]
    probes = [tools.Probe(pos, maxTime) for pos in probesPos]

    # Положение начала диэлектрика
    layer_1_x = 100
    layer_2_x = 300

    # Параметры среды
    # Диэлектрическая проницаемость
    eps = numpy.ones(maxSize)
    eps[layer_1_x: layer_2_x] = 9.0

    # Магнитная проницаемость
    mu = numpy.ones(maxSize)
    # mu[layer_1_x: layer_2_x] = 9.0

    ScE = numpy.sqrt(eps * mu)
    ScH = numpy.sqrt(eps * mu)
    ScH[layer_2_x - 1] = 1.0

    Ez = numpy.zeros(maxSize)
    Hy = numpy.zeros(maxSize)

    source = GaussianPlaneWave(30.0, 10.0)

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
    display.drawBoundary(layer_1_x)
    display.drawBoundary(layer_2_x)

    for q in range(maxTime):
        # Граничные условия для поля H
        Hy[-1] = Hy[-2]

        # Расчет компоненты поля H
        Ez_shift = Ez[1:]
        Hy[:-1] = Hy[:-1] + (Ez_shift - Ez[:-1]) * ScH[:-1] / (W0 * mu[:-1])

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Hy[sourcePos - 1] -= (ScH[sourcePos - 1] / (W0 * mu[sourcePos - 1])) * source.getE(0, q)

        # Граничные условия для поля E
        Ez[0] = Ez[1]

        # Расчет компоненты поля E
        Hy_shift = Hy[:-1]
        Ez[1:] = Ez[1:] + (Hy[1:] - Hy_shift) * ScE[1:] * W0 / eps[1:]

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Ez[sourcePos] += ((ScE[sourcePos] / (numpy.sqrt(eps[sourcePos] * mu[sourcePos]))) *
                          source.getE(-0.5, q + 0.5))

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(display_field, q)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    tools.showProbeSignals(probes, -1.1, 1.1)
