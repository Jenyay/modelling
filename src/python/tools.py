# -*- coding: utf-8 -*-
'''
Модуль со вспомогательными классами и функциями, не связанные напрямую с
методом FDTD
'''

from typing import List

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt


class Probe:
    '''
    Класс для хранения временного сигнала в датчике.
    '''
    def __init__(self, position: int, maxTime: int):
        '''
        position - положение датчика (номер ячейки).
        maxTime - максимальное количество временных
            шагов для хранения в датчике.
        '''
        self.position = position

        # Временные сигналы для полей E и H
        self.E = np.zeros(maxTime)
        self.H = np.zeros(maxTime)

        # Номер временного шага для сохранения полей
        self._time = 0

    def addData(self, E: npt.NDArray, H: npt.NDArray):
        '''
        Добавить данные по полям E и H в датчик.
        '''
        self.E[self._time] = E[self.position]
        self.H[self._time] = H[self.position]
        self._time += 1


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
        self._xdata = None
        self._line = None
        self._xlabel = 'x, отсчет'
        self._ylabel = yLabel
        self._probeStyle = 'xr'
        self._sourceStyle = 'ok'

    def activate(self):
        '''
        Инициализировать окно с анимацией
        '''
        self._xdata = np.arange(self._maxXSize)

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
        self._line = self._ax.plot(self._xdata, np.zeros(self._maxXSize))[0]

    def drawProbes(self, probesPos: List[int]):
        '''
        Нарисовать датчики.

        probesPos - список координат датчиков для регистрации временных
            сигналов (в отсчетах).
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

    def drawBoundary(self, position: int):
        '''
        Нарисовать границу в области моделирования.

        position - координата X границы (в отсчетах).
        '''
        self._ax.plot([position, position],
                      [self._minYSize, self._maxYSize],
                      '--k')

    def stop(self):
        '''
        Остановить анимацию
        '''
        plt.ioff()

    def updateData(self, data: npt.NDArray, timeCount: int):
        '''
        Обновить данные с распределением поля в пространстве
        '''
        self._line.set_ydata(data)
        self._ax.set_title(str(timeCount))
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

class AnimateFieldDisplayEH:
    '''
    Класс для отображения анимации распространения ЭМ волны в пространстве
    '''

    def __init__(self,
                 maxXSize: int,
                 minYSizeE: float, maxYSizeE: float):
        '''
        maxXSize - размер области моделирования в отсчетах.
        minYSizeE, maxYSizeE - интервал отображения графика по оси Y.
        '''
        W0 = 120.0 * np.pi
        self._maxXSize = maxXSize
        self._minYSize_E = minYSizeE
        self._maxYSize_E = maxYSizeE
        self._minYSize_H = minYSizeE / W0
        self._maxYSize_H = maxYSizeE / W0
        self._xdata_E = None
        self._xdata_H = None
        self._line_E = None
        self._line_H = None
        self._ax_E = None
        self._ax_H = None
        self._xlabel = 'x, отсчет'
        self._ylabel_E = 'Ez, В/м'
        self._ylabel_H = 'Hy, А/м'
        self._probeStyle = 'xr'
        self._sourceStyle = 'ok'

    def activate(self):
        '''
        Инициализировать окно с анимацией
        '''
        self._xdata_E = np.arange(self._maxXSize)
        self._xdata_H = np.arange(self._maxXSize)

        # Включить интерактивный режим для анимации
        plt.ion()

        # Создание окна для графика
        self._fig, (self._ax_E, self._ax_H) = plt.subplots(nrows=2)

        # Установка отображаемых интервалов по осям
        self._ax_E.set_xlim(0, self._maxXSize)
        self._ax_E.set_ylim(self._minYSize_E, self._maxYSize_E)
        self._ax_H.set_xlim(0, self._maxXSize)
        self._ax_H.set_ylim(self._minYSize_H, self._maxYSize_H)

        # Установка меток по осям
        self._ax_E.set_xlabel(self._xlabel)
        self._ax_E.set_ylabel(self._ylabel_E)
        self._ax_H.set_xlabel(self._xlabel)
        self._ax_H.set_ylabel(self._ylabel_H)

        # Включить сетку на графике
        self._ax_E.grid()
        self._ax_H.grid()

        # Отобразить поле в начальный момент времени
        self._line_E = self._ax_E.plot(self._xdata_E, np.zeros(self._maxXSize), '-b')[0]
        self._line_H = self._ax_H.plot(self._xdata_H, np.zeros(self._maxXSize), '-r')[0]

    def drawProbes(self, probesPos: List[int]):
        '''
        Нарисовать датчики.

        probesPos - список координат датчиков для регистрации временных
            сигналов (в отсчетах).
        '''
        # Отобразить положение датчиков
        self._ax_E.plot(probesPos, [0] * len(probesPos), self._probeStyle)
        self._ax_H.plot(probesPos, [0] * len(probesPos), self._probeStyle)

    def drawSources(self, sourcesPos: List[int]):
        '''
        Нарисовать источники.

        sourcesPos - список координат источников (в отсчетах).
        '''
        # Отобразить положение источников
        self._ax_E.plot(sourcesPos, [0] * len(sourcesPos), self._sourceStyle)
        self._ax_H.plot(sourcesPos, [0] * len(sourcesPos), self._sourceStyle)

    def drawBoundary(self, position: int):
        '''
        Нарисовать границу в области моделирования.

        position - координата X границы (в отсчетах).
        '''
        self._ax_E.plot([position, position],
                      [self._minYSize_E, self._maxYSize_E],
                      '--k')
        self._ax_H.plot([position, position],
                      [self._minYSize_H, self._maxYSize_H],
                      '--k')

    def stop(self):
        '''
        Остановить анимацию
        '''
        plt.ioff()

    def updateData(self, E: npt.NDArray, H: npt.NDArray, timeCount: int):
        '''
        Обновить данные с распределением поля в пространстве
        '''
        self._line_E.set_ydata(E)
        self._line_H.set_ydata(H)
        self._ax_E.set_title(str(timeCount))
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

def showProbeSignals(probes: List[Probe], minYSize: float, maxYSize: float):
    '''
    Показать графики сигналов, зарегистрированых в датчиках.

    probes - список экземпляров класса Probe.
    minYSize, maxYSize - интервал отображения графика по оси Y.
    '''
    # Создание окна с графиков
    fig, ax = plt.subplots()

    # Настройка внешнего вида графиков
    ax.set_xlim(0, len(probes[0].E))
    ax.set_ylim(minYSize, maxYSize)
    ax.set_xlabel('q, отсчет')
    ax.set_ylabel('Ez, В/м')
    ax.grid()

    # Вывод сигналов в окно
    for probe in probes:
        ax.plot(probe.E)

    # Создание и отображение легенды на графике
    legend = ['Probe x = {}'.format(probe.position) for probe in probes]
    ax.legend(legend)

    # Показать окно с графиками
    plt.show()
