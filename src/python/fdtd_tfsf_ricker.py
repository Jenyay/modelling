# -*- coding: utf-8 -*-
'''
Вейвлет Рикера распространяется в одну сторону (TFSF boundary).
Область моделирования - свободное пространство.
'''

import numpy as np

import tools


if __name__ == '__main__':
    # Характеристическое сопротивление свободного пространства
    Z0 = 120.0 * np.pi

    # Число Куранта
    Sc = 1.0

    # Время расчета в отсчетах
    maxTime = 400

    # Размер области моделирования в отсчетах
    maxSize = 200

    # Положение источника в отсчетах
    sourcePos = 20

    # Параметры Вейвлета Рикера
    Np = 30
    Md = 2.5

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

    for q in range(maxTime):
        # Расчет компоненты поля H
        Hy[:] = Hy + (Ez[1:] - Ez[:-1]) * Sc / (Z0 * mu)

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Hy[sourcePos - 1] -= ((1 - 2 * (np.pi ** 2) * (Sc * q / Np - Md) ** 2) *
                              np.exp(-np.pi ** 2 * (Sc * q / Np - Md) ** 2) / Z0)

        Ez[0] = Ez[1]
        Ez[-1] = Ez[-2]

        # Расчет компоненты поля E
        Ez[1:-1] = Ez[1:-1] + (Hy[1:] - Hy[:-1]) * Sc * Z0 / eps[1:-1]

        # Источник возбуждения с использованием метода
        # Total Field / Scattered Field
        Ez[sourcePos] += ((1 - 2 * np.pi ** 2 * ((Sc * (q + 0.5) - (-0.5)) / Np - Md) ** 2) *
                          np.exp(-np.pi ** 2 * ((Sc * (q + 0.5) - (-0.5)) / Np - Md) ** 2))

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(display_field, q)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    tools.showProbeSignals(probes, -1.1, 1.1)
