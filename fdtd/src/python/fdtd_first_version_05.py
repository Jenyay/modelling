# coding: utf-8
'''
История изменений:
    * Работа с датчиками вынесена в класс Probe.
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


class Probe:
    '''
    Класс для хранения временного сигнала в датчике.
    '''

    def __init__(self, position: int, maxTime: int):
        '''
        position - положение датчика (номер ячейки)
        maxTime - максимальное количество временных шагов для хранения в датчике
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
        self.maxXSize = maxXSize
        self.minYSize = minYSize
        self.maxYSize = maxYSize
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
        self._xList = np.arange(self.maxXSize)

        # Включить интерактивный режим для анимации
        plt.ion()

        # Создание окна для графика
        self._fig, self._ax = plt.subplots()

        # Установка отображаемых интервалов по осям
        self._ax.set_xlim(0, self.maxXSize)
        self._ax.set_ylim(self.minYSize, self.maxYSize)

        # Установка меток по осям
        self._ax.set_xlabel(self._xlabel)
        self._ax.set_ylabel(self._ylabel)

        # Включить сетку на графике
        self._ax.grid()

        # Отобразить поле в начальный момент времени
        self._line, = self._ax.plot(self._xList, np.zeros(self.maxXSize))

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

    def updateData(self, data):
        '''
        Обновить данные с распределением поля в пространстве
        '''
        self._line.set_ydata(data)
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()


def showProbeSignals(probes: List[Probe], minYSize: float, maxYSize: float):
    '''
    Показать графики сигналов, зарегистрированых в датчиках.

    probes - список экземпляров класса Probe.
    minYSize, maxYSize - интервал отображения графика по оси Y.
    '''
    # Создание окна с графиками
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


if __name__ == '__main__':
    # Волновое сопротивление свободного пространства
    W0 = 120.0 * np.pi

    # Число Куранта
    Sc = 1.0

    # Время расчета в отсчетах
    maxTime = 1000

    # Размер области моделирования в отсчетах
    maxSize = 200

    # Датчики для регистрации поля
    probesPos = [50, 100]
    probes = [Probe(pos, maxTime) for pos in probesPos]

    # Положение источника
    sourcePos = 75

    Ez = np.zeros(maxSize)
    Hy = np.zeros(maxSize)

    for probe in probes:
        probe.addData(Ez, Hy)

    # Создание экземпляра класса для отображения
    # распределения поля в пространстве
    display = AnimateFieldDisplay(maxSize, -1.1, 1.1, 'Ez, В/м')
    display.activate()
    display.drawSources([sourcePos])
    display.drawProbes(probesPos)

    for q in range(1, maxTime):
        # Расчет компоненты поля H
        Hy[:-1] = Hy[:-1] + (Ez[1:] - Ez[:-1]) * Sc / W0

        # Расчет компоненты поля E
        Ez[1:] = Ez[1:] + (Hy[1:] - Hy[:-1]) * Sc * W0

        # Источник возбуждения
        Ez[sourcePos] += np.exp(-(q - 0.5 - 30.0) ** 2 / 100.0)

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(Ez)

    display.stop()

    # Отображение сигнала, сохраненного в датчиках
    showProbeSignals(probes, -1.1, 1.1)
