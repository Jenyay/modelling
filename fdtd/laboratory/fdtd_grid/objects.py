import numpy as np
import numpy.typing as npt

from typing import Optional, List


class LayerContinuous:
    def __init__(self,
                 xmin: float,
                 xmax: Optional[float] = None,
                 eps: float = 1.0,
                 mu: float = 1.0,
                 sigma: float = 0.0):
        self.xmin = xmin
        self.xmax = xmax
        self.eps = eps
        self.mu = mu
        self.sigma = sigma


class LayerDiscrete:
    def __init__(self,
                 xmin: int,
                 xmax: Optional[int] = None,
                 eps: float = 1.0,
                 mu: float = 1.0,
                 sigma: float = 0.0):
        self.xmin = xmin
        self.xmax = xmax
        self.eps = eps
        self.mu = mu
        self.sigma = sigma


class Probe:
    '''
    Класс для хранения временного сигнала в пробнике.
    '''

    def __init__(self, position: int, maxTime: int):
        '''
        position - положение пробника (номер ячейки).
        maxTime - максимально количество временных шагов для хранения в пробнике.
        '''
        self.position = position

        # Временные сигналы для полей E и H
        self.E = np.zeros(maxTime)
        self.H = np.zeros(maxTime)

        # Номер временного шага для сохранения полей
        self._time = 0

    def addData(self, E: npt.NDArray[float], H: npt.NDArray[float]):
        '''
        Добавить данные по полям E и H в пробник.
        '''
        self.E[self._time] = E[self.position]
        self.H[self._time] = H[self.position]
        self._time += 1
