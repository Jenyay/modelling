# -*- coding: utf-8 -*-
'''
Модуль со вспомогательными классами и функциями, не связанные напрямую с
методом FDTD
'''

import pylab
import numpy as np
import numpy.typing as npt
from typing import List, Optional

from objects import Probe


class AnimateFieldDisplay:
    '''
    Класс для отображения анимации распространения ЭМ волны в пространстве
    '''

    def __init__(self,
                 dx: float,
                 dt: float,
                 maxXSize: int,
                 minYSize: float, maxYSize: float,
                 yLabel: str,
                 title: Optional[str] = None
                 ):
        '''
        dx - дискрет по простарнству, м
        dt - дискрет по времени, сек
        maxXSize - размер области моделирования в отсчетах.
        minYSize, maxYSize - интервал отображения графика по оси Y.
        yLabel - метка для оси Y
        '''
        self.maxXSize = maxXSize
        self.minYSize = minYSize
        self.maxYSize = maxYSize
        self._xList = None
        self._line = None
        self._xlabel = 'x, м'
        self._ylabel = yLabel
        self._probeStyle = 'xr'
        self._sourceStyle = 'ok'
        self._dx = dx
        self._dt = dt
        self._title = title

    def activate(self):
        '''
        Инициализировать окно с анимацией
        '''
        self._xList = np.arange(self.maxXSize) * self._dx

        # Включить интерактивный режим для анимации
        pylab.ion()

        # Создание окна для графика
        self._fig, self._ax = pylab.subplots(
            figsize=(10, 6.5))

        if self._title is not None:
            self._fig.suptitle(self._title)

        # Установка отображаемых интервалов по осям
        self._ax.set_xlim(0, self.maxXSize * self._dx)
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
        Нарисовать пробники.

        probesPos - список координат пробников для регистрации временных
            сигналов (в отсчетах).
        '''
        # Отобразить положение пробника
        self._ax.plot(np.array(probesPos) * self._dx,
                      [0] * len(probesPos), self._probeStyle)

        for n, pos in enumerate(probesPos):
            self._ax.text(
                pos * self._dx,
                0,
                '\n{n}'.format(n=n + 1),
                verticalalignment='top',
                horizontalalignment='center')

    def drawSources(self, sourcesPos: List[int]):
        '''
        Нарисовать источники.

        sourcesPos - список координат источников (в отсчетах).
        '''
        # Отобразить положение пробника
        self._ax.plot(np.array(sourcesPos) * self._dx,
                      [0] * len(sourcesPos), self._sourceStyle)

    def drawBoundary(self, position: int):
        '''
        Нарисовать границу в области моделирования.

        position - координата X границы (в отсчетах).
        '''
        self._ax.plot([position * self._dx, position * self._dx],
                      [self.minYSize, self.maxYSize],
                      '--k')

    def stop(self):
        '''
        Остановить анимацию
        '''
        pylab.ioff()

    def updateData(self, data: npt.NDArray[float], timeCount: int):
        '''
        Обновить данные с распределением поля в пространстве
        '''
        self._line.set_ydata(data)
        time_str = '{:.5f}'.format(timeCount * self._dt * 1e9)
        self._ax.set_title(f'{time_str} нс')
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()


def showProbeSignals(probes: List[Probe],
                     dx: float, dt: float, minYSize: float, maxYSize: float):
    '''
    Показать графики сигналов, зарегистрированых в датчиках.

    probes - список экземпляров класса Probe.
    dx - дискрет по пространству, м
    dt - дискрет по времени, с
    minYSize, maxYSize - интервал отображения графика по оси Y.
    '''
    # Создание окна с графиков
    fig, axes_list = pylab.subplots(nrows=len(probes),
                                    figsize=(10, 6.5),
                                    tight_layout={'w_pad': 0.7, 'h_pad': 0.7})
    fig.suptitle('Сигналы в датчиках')

    # legends = []
    # Вывод сигналов в окно
    for n, (probe, ax) in enumerate(zip(probes, axes_list)):
        # Настройка внешнего вида графиков
        ax.set_xlim(0, len(probes[0].E) * dt * 1e9)
        ax.set_ylim(minYSize, maxYSize)
        ax.set_xlabel('t, нс')
        ax.set_ylabel('Ez, В/м')
        ax.grid()

        time_list = np.arange(len(probe.E)) * dt * 1e9
        maxval = np.max(probe.E)
        minval = np.min(probe.E)
        legend = 'Датчик {n}: x = {pos:.5f}; Max = {maxval:.5f}; Min = {minval:.5f}'.format(
            n=n + 1, pos=probe.position * dx, maxval=maxval, minval=minval)
        # legends.append(legend)
        ax.plot(time_list, probe.E)

        # Создание и отображение легенды на графике
        legend_obj = ax.legend([legend])
        legend_obj.set_draggable(True)

    # Показать окно с графиками
    pylab.show()
