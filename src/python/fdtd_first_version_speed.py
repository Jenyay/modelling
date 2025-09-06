# coding: utf-8
'''
Расчет скорости распространения ЭМ волны в свободном пространстве
'''

import numpy

import tools


if __name__ == '__main__':
    # Характеристическое сопротивление свободного пространства
    Z0 = 120.0 * numpy.pi

    # Число Куранта
    Sc = 1.0

    # Время расчета в отсчетах
    maxTime = 250

    # Размер области моделирования в отсчетах
    maxSize = 200

    # Датчики для регистрации поля
    probePos = [50, 150]
    probes = [tools.Probe(pos, maxTime) for pos in probePos]

    # Положение источника
    sourcePos = 25

    Ez = numpy.zeros(maxSize)
    Hy = numpy.zeros(maxSize)

    for probe in probes:
        probe.addData(Ez, Hy)

    # Создание экземпляра класса для отображения
    # распределения поля в пространстве
    display = tools.AnimateFieldDisplay(maxSize, -1.1, 1.1, 'Ez, В/м')
    display.activate()
    display.drawSources([sourcePos])
    display.drawProbes(probePos)

    for q in range(1, maxTime):
        # Расчет компоненты поля H
        Hy[:-1] = Hy[:-1] + (Ez[1:] - Ez[:-1]) * Sc / Z0

        # Расчет компоненты поля E
        Ez[1:] = Ez[1:] + (Hy[1:] - Hy[:-1]) * Sc * Z0

        # Источник возбуждения
        Ez[sourcePos] += numpy.exp(-(q - 0.5 - 30.0) ** 2 / 100.0)

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(Ez, q)

    display.stop()

    # Отображение сигнала, сохраненного в пробниках
    tools.showProbeSignals(probes, -1.1, 1.1)
