# -*- coding: utf-8 -*-
'''
Моделирование распространения ЭМ волны, падающей на границу
вакуум - идеальный диэлектрик.
Используются граничные условия ABC второй степени.
'''

import numpy as np

import tools


class HarmonicPlaneWave:
    ''' Класс с уравнением плоской волны для гармонического сигнала в дискретном виде
    Nl - количество ячеек на длину.
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
    maxTime = 1000

    # Размер области моделирования в отсчетах
    maxSize = 300

    # Положение источника в отсчетах
    sourcePos = 50

    # Датчики для регистрации поля
    probesPos = [220]
    probes = [tools.Probe(pos, maxTime) for pos in probesPos]

    # Положение начала диэлектрика
    layer_x = 250

    # Количество отсчетов на длину волны
    Nl = 50

    # Начальная фаза
    phi0 = -2 * np.pi / Nl

    # Параметры среды
    # Диэлектрическая проницаемость
    eps = np.ones(maxSize)
    eps[layer_x:] = 2.0

    # Магнитная проницаемость
    mu = np.ones(maxSize - 1)

    Ez = np.zeros(maxSize)
    Hy = np.zeros(maxSize - 1)

    source = HarmonicPlaneWave(Nl, phi0, Sc)

    # Коэффициенты для расчета ABC второй степени
    # Sc' для левой границы
    Sc1Left = Sc / np.sqrt(mu[0] * eps[0])

    k1Left = -1 / (1 / Sc1Left + 2 + Sc1Left)
    k2Left = 1 / Sc1Left - 2 + Sc1Left
    k3Left = 2 * (Sc1Left - 1 / Sc1Left)
    k4Left = 4 * (1 / Sc1Left + Sc1Left)

    # Sc' для правой границы
    Sc1Right = Sc / np.sqrt(mu[-1] * eps[-1])

    k1Right = -1 / (1 / Sc1Right + 2 + Sc1Right)
    k2Right = 1 / Sc1Right - 2 + Sc1Right
    k3Right = 2 * (Sc1Right - 1 / Sc1Right)
    k4Right = 4 * (1 / Sc1Right + Sc1Right)

    # Ez[0: 2] в предыдущий момент времени (q)
    oldEzLeft1 = np.zeros(3)

    # Ez[0: 2] в пред-предыдущий момент времени (q - 1)
    oldEzLeft2 = np.zeros(3)

    # Ez[-3: -1] в предыдущий момент времени (q)
    oldEzRight1 = np.zeros(3)

    # Ez[-3: -1] в пред-предыдущий момент времени (q - 1)
    oldEzRight2 = np.zeros(3)

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
    display.drawBoundary(layer_x)

    for q in range(1, maxTime):
        # Расчет компоненты поля H
        Hy = Hy + (Ez[1:] - Ez[:-1]) * Sc / (W0 * mu)

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Hy[sourcePos - 1] -= (Sc / W0) * source.getE(0, q)

        # Расчет компоненты поля E
        Hy_shift = Hy[: -1]
        Ez[1:-1] = Ez[1: -1] + (Hy[1:] - Hy_shift) * Sc * W0 / eps[1: -1]

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Ez[sourcePos] += Sc * source.getE(-0.5, q + 0.5)

        # Граничные условия ABC второй степени (слева)
        Ez[0] = (k1Left * (k2Left * (Ez[2] + oldEzLeft2[0]) +
                           k3Left * (oldEzLeft1[0] + oldEzLeft1[2] - Ez[1] - oldEzLeft2[1]) -
                           k4Left * oldEzLeft1[1]) - oldEzLeft2[2])

        oldEzLeft2[:] = oldEzLeft1[:]
        oldEzLeft1[:] = Ez[0: 3]

        # Граничные условия ABC второй степени (справа)
        Ez[-1] = (k1Right * (k2Right * (Ez[-3] + oldEzRight2[-1]) +
                             k3Right * (oldEzRight1[-1] + oldEzRight1[-3] - Ez[-2] - oldEzRight2[-2]) -
                             k4Right * oldEzRight1[-2]) - oldEzRight2[-3])

        oldEzRight2[:] = oldEzRight1[:]
        oldEzRight1[:] = Ez[-3:]

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(display_field, q)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    tools.showProbeSignals(probes, -2.1, 2.1)
