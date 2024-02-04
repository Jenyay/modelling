# -*- coding: utf-8 -*-
'''
Синусоидальный сигнал распространяется в одну сторону (TFSF boundary).
Область моделирования - свободное пространство.
'''

import numpy as np

import tools


class HarmonicPlaneWave:
    ''' Класс с уравнением плоской волны для гармонического сигнала в дискретном виде
    Nl - количество ячеек на длину волны.
    phi0 - начальная фаза.
    Sc - число Куранта.
    eps - относительная диэлектрическая проницаемость среды, в которой расположен источник.
    mu - относительная магнитная проницаемость среды, в которой расположен источник.
    '''

    def __init__(self, Nl, phi0, Sc=1.0, eps=1.0, mu=1.0):
        self.Nl = Nl
        self.phi0 = phi0
        self.Sc = Sc
        self.eps = eps
        self.mu = mu

    def getE(self, m, q):
        '''
        Расчет поля E в дискретной точке пространства m
        в дискретный момент времени q
        '''
        return np.sin(2 * np.pi / self.Nl * (self.Sc * q - np.sqrt(self.mu * self.eps) * m) + self.phi0)


if __name__ == '__main__':
    # Волновое сопротивление свободного пространства
    W0 = 120.0 * np.pi

    # Число Куранта
    Sc = 1.0

    # Время расчета в отсчетах
    maxTime = 700

    # Размер области моделирования в отсчетах
    maxSize = 200

    # Положение источника в отсчетах
    sourcePos = 20

    # Параметры гармонического сигнала
    # Количество ячеек на длину волны
    Nl = 50

    phi0 = -2 * np.pi / Nl
    # phi0 = 0

    # Датчики для регистрации поля
    probesPos = [60]
    probes = [tools.Probe(pos, maxTime) for pos in probesPos]

    # Параметры среды
    # Диэлектрическая проницаемость
    eps = np.ones(maxSize)

    # Магнитная проницаемость
    mu = np.ones(maxSize - 1)

    Ez = np.zeros(maxSize)
    Hy = np.zeros(maxSize - 1)

    source = HarmonicPlaneWave(Nl, phi0, Sc)

    # Параметры отображения поля E
    display_field = Ez
    display_ylabel = 'Ez, В/м'
    display_ymin = -2.1
    display_ymax = 2.1

    # Создание экземпляра класса для отображения
    # распределения поля в пространстве
    display = tools.AnimateFieldDisplay(maxSize,
                                        display_ymin, display_ymax,
                                        display_ylabel)

    display.activate()
    display.drawProbes(probesPos)
    display.drawSources([sourcePos])

    for q in range(1, maxTime):
        # Расчет компоненты поля H
        Hy = Hy + (Ez[1:] - Ez[:-1]) * Sc / (W0 * mu)

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Hy[sourcePos - 1] -= (Sc / (W0 * mu[sourcePos])) * source.getE(0, q)

        Ez[0] = Ez[1]
        Ez[-1] = Ez[-2]

        # Расчет компоненты поля E
        Ez[1:-1] = Ez[1:-1] + (Hy[1:] - Hy[:-1]) * Sc * W0 / eps[1:-1]

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Ez[sourcePos] += (Sc / np.sqrt(eps[sourcePos] * mu[sourcePos])) * source.getE(-0.5, q + 0.5)

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(display_field, q)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    tools.showProbeSignals(probes, -2.1, 2.1)
