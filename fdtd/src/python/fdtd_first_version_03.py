# coding: utf-8
'''
История изменений:
    * Циклы по пространству заменены на векторизованные операции с массивами.
    * Добавлена анимация поля E.
    * Первая версия программы с использованием метода FDTD.
'''

import matplotlib.pyplot as plt
import numpy


if __name__ == '__main__':
    # Волновое сопротивление свободного пространства
    W0 = 120.0 * numpy.pi

    # Число Куранта
    Sc = 1.0

    # Время расчета в отсчетах
    maxTime = 1000

    # Размер области моделирования в отсчетах
    maxSize = 200

    # Положение датчика, регистрирующего поле
    probePos = 50

    # Положение источника
    sourcePos = 75

    Ez = numpy.zeros(maxSize)
    Hy = numpy.zeros(maxSize)

    # Поле, зарегистрированное в датчике в зависимости от времени
    probeTimeEz = numpy.zeros(maxTime)
    probeTimeEz[0] = Ez[probePos]

    # Подготовка к отображению поля в пространстве
    xlist = numpy.arange(maxSize)

    # Включить интерактивный режим для анимации
    plt.ion()

    # Создание окна для графика
    fig, ax = plt.subplots()

    # Установка отображаемых интервалов по осям
    ax.set_xlim(0, maxSize)
    ax.set_ylim(-1.1, 1.1)

    # Установка меток по осям
    ax.set_xlabel('x, отсчет')
    ax.set_ylabel('Ez, В/м')

    # Включить сетку на графике
    ax.grid()

    # Отобразить поле в начальный момент времени
    line, = ax.plot(xlist, Ez)

    # Отобразить положение источника
    ax.plot(sourcePos, 0, 'ok')

    # Отобразить положение датчика
    ax.plot(probePos, 0, 'xr')

    for q in range(1, maxTime):
        # Расчет компоненты поля H
        Hy[:-1] = Hy[:-1] + (Ez[1:] - Ez[:-1]) * Sc / W0

        # Расчет компоненты поля E
        Ez[1:] = Ez[1:] + (Hy[1:] - Hy[:-1]) * Sc * W0

        # Источник возбуждения
        Ez[sourcePos] += numpy.exp(-(q - 0.5 - 30.0) ** 2 / 100.0)

        # Регистрация поля в точке
        probeTimeEz[q] = Ez[probePos]

        if q % 2 == 0:
            # Обновить данные на графике
            line.set_ydata(Ez)
            fig.canvas.draw()
            fig.canvas.flush_events()

    # Отключить интерактивный режим по завершению анимации
    plt.ioff()

    # Отображение сигнала, сохраненного в датчике
    tlist = numpy.arange(maxTime)
    fig, ax = plt.subplots()
    ax.set_xlim(0, maxTime)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel('x, отсчет')
    ax.set_ylabel('Ez, В/м')
    ax.plot(tlist, probeTimeEz)
    ax.grid()
    plt.show()
