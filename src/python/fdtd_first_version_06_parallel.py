# coding: utf-8
'''
История изменений:
    * Функции и классы, не связанные напрямую с методом FDTD,
        вынесены в модуль tools.
    * Работа с датчиками вынесена в класс Probe.
    * Рисование графиков вынесено в класс AnimateFieldDisplay и функцию
        showProbeSignals.
    * Циклы по пространству заменены на векторизованные операции с массивами.
    * Добавлена анимация поля E.
    * Первая версия программы с использованием метода FDTD.
'''

# import os

# os.environ['NUMEXPR_MAX_THREADS'] = '24'
# os.environ['NUMEXPR_NUM_THREADS'] = '24'

import numpy as np
import numexpr as ne

import tools


if __name__ == '__main__':
    # Волновое сопротивление свободного пространства
    W0 = 120.0 * np.pi

    # Число Куранта
    Sc = 1.0

    # Время расчета в отсчетах
    maxTime = 1000

    # Размер области моделирования в отсчетах
    maxSize = 2000000

    # Датчики для регистрации поля
    probesPos = [50, 100]
    probes = [tools.Probe(pos, maxTime) for pos in probesPos]

    # Положение источника
    sourcePos = 75

    Ez = np.zeros(maxSize)
    Hy = np.zeros(maxSize)

    for probe in probes:
        probe.addData(Ez, Hy)

    # Создание экземпляра класса для отображения
    # распределения поля в пространстве
    display = tools.AnimateFieldDisplay(maxSize, -1.1, 1.1, 'Ez, В/м')
    display.activate()
    display.drawSources([sourcePos])
    display.drawProbes(probesPos)

    for q in range(1, maxTime):
        # Расчет компоненты поля H
        Hy[:-1] = ne.evaluate('Hy_old + (Ez_left - Ez_right) * Sc / W0', 
                              global_dict={
                                  'Hy_old': Hy[:-1],
                                  'Ez_left': Ez[1:],
                                  'Ez_right': Ez[:-1]
                                  }
                              )
        # Hy[:-1] = Hy[:-1] + (Ez[1:] - Ez[:-1]) * Sc / W0

        # Расчет компоненты поля E
        Ez[1:] = ne.evaluate('Ez_old + (Hy_right - Hy_left) * Sc * W0', 
                             global_dict={
                                 'Ez_old': Ez[1:],
                                 'Hy_right': Hy[1:],
                                 'Hy_left': Hy[:-1]
                                 }
                             )
        # Ez[1:] = Ez[1:] + (Hy[1:] - Hy[:-1]) * Sc * W0

        # Источник возбуждения
        Ez[sourcePos] += np.exp(-(q - 0.5 - 30.0) ** 2 / 100.0)

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        # if q % 2 == 0:
        #     display.updateData(Ez, q)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    # tools.showProbeSignals(probes, -1.1, 1.1)
