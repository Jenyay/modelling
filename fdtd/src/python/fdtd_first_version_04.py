# coding: utf-8
'''
История изменений:
    * Рисование графиков вынесено в класс AnimateFieldDisplay
        и функцию showProbeSignals.
    * Циклы по пространству заменены на векторизованные операции с массивами.
    * Добавлена анимация поля E.
    * Первая версия программы с использованием метода FDTD.
'''

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from typing import List


class AnimateFieldDisplay:
    '''
    Класс для отображения анимации распространения ЭМ волны в пространстве
    '''

    def __init__(self,
                 maxXSize: int,
                 minYSize: float, maxYSize: float,
                 yLabel: str):
        '''
        maxXSize - размер области моделирования в отсчетах.
        minYSize, maxYSize - интервал отображения графика по оси Y.
        yLabel - метка для оси Y
        '''
        self._maxXSize = maxXSize
        self._minYSize = minYSize
        self._maxYSize = maxYSize
        self._xList = None
        self._line = None
        self._xlabel = 'x, отсчет'
        self._ylabel = yLabel
        self._probeStyle = 'xr'
        self._sourceStyle = 'ok'

    def activate(self):
        '''
        Инициализировать окно с анимацией
        '''
        self._xList = np.arange(self._maxXSize)

        # Включить интерактивный режим для анимации
        plt.ion()

        # Создание окна для графика
        self._fig, self._ax = plt.subplots()

        # Установка отображаемых интервалов по осям
        self._ax.set_xlim(0, self._maxXSize)
        self._ax.set_ylim(self._minYSize, self._maxYSize)

        # Установка меток по осям
        self._ax.set_xlabel(self._xlabel)
        self._ax.set_ylabel(self._ylabel)

        # Включить сетку на графике
        self._ax.grid()

        # Отобразить поле в начальный момент времени
        self._line = self._ax.plot(self._xList, np.zeros(self._maxXSize))[0]

    def drawProbes(self, probesPos: List[int]):
        '''
        probesPos - список координат датчиков для регистрации временных
            сигналов.
        '''
        # Отобразить положение датчиков
        self._ax.plot(probesPos, [0] * len(probesPos), self._probeStyle)

    def drawSources(self, sourcesPos: List[int]):
        '''
        Нарисовать источники.

        sourcesPos - список координат источников (в отсчетах).
        '''
        # Отобразить положение источников
        self._ax.plot(sourcesPos, [0] * len(sourcesPos), self._sourceStyle)

    def stop(self):
        '''
        Остановить анимацию
        '''
        plt.ioff()

    def updateData(self, data: npt.NDArray):
        '''
        Обновить данные с распределением поля в пространстве
        '''
        self._line.set_ydata(data)
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()


def showProbeSignals(signals: List[npt.NDArray],
                     minYSize: float,
                     maxYSize: float):
    '''
    Показать графики сигналов, зарегистрированых в датчиках.

    signals - список сигналов, зарегистрированных датчиками.
    minYSize, maxYSize - интервал отображения графика по оси Y.
    '''
    fig, ax = plt.subplots()
    ax.set_xlim(0, len(signals[0]))
    ax.set_ylim(minYSize, maxYSize)
    ax.set_xlabel('q, отсчет')
    ax.set_ylabel('Ez, В/м')
    ax.grid()

    for signal in signals:
        ax.plot(signal)

    plt.show()


if __name__ == '__main__':
    # Волновое сопротивление свободного пространства
    W0 = 120.0 * np.pi

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

    Ez = np.zeros(maxSize)
    Hy = np.zeros(maxSize)

    # Поле, зарегистрированное в датчике в зависимости от времени
    probeTimeEz = np.zeros(maxTime)
    probeTimeEz[0] = Ez[probePos]

    # Создание экземпляра класса для отображения
    # распределения поля в пространстве
    display = AnimateFieldDisplay(maxSize, -1.1, 1.1, 'Ez, В/м')
    display.activate()
    display.drawSources([sourcePos])
    display.drawProbes([probePos])

    for q in range(1, maxTime):
        # Расчет компоненты поля H
        Hy[:-1] = Hy[:-1] + (Ez[1:] - Ez[:-1]) * Sc / W0

        # Расчет компоненты поля E
        Ez[1:] = Ez[1:] + (Hy[1:] - Hy[:-1]) * Sc * W0

        # Источник возбуждения
        Ez[sourcePos] += np.exp(-(q - 0.5 - 30.0) ** 2 / 100.0)

        # Регистрация поля в точке
        probeTimeEz[q] = Ez[probePos]

        if q % 2 == 0:
            display.updateData(Ez)

    display.stop()

    # Отображение сигнала, сохраненного в датчике
    showProbeSignals([probeTimeEz], -1.1, 1.1)
