from abc import ABCMeta, abstractmethod

import numpy


class BoundaryBase(metaclass=ABCMeta):
    @abstractmethod
    def updateField(self, E, H):
        pass


class ABCSecondBase(BoundaryBase, metaclass=ABCMeta):
    '''
    Поглощающие граничные условия второй степени
    '''
    def __init__(self, eps, mu, Sc):
        Sc1 = Sc / numpy.sqrt(mu * eps)
        self.k1 = -1 / (1 / Sc1 + 2 + Sc1)
        self.k2 = 1 / Sc1 - 2 + Sc1
        self.k3 = 2 * (Sc1 - 1 / Sc1)
        self.k4 = 4 * (1 / Sc1 + Sc1)

        # E в предыдущий момент времени (q)
        self.oldE1 = numpy.zeros(3)

        # E в пред-предыдущий момент времени (q - 1)
        self.oldE2 = numpy.zeros(3)


class ABCSecondLeft(ABCSecondBase):
    def updateField(self, E, H):
        E[0] = (self.k1 * (self.k2 * (E[2] + self.oldE2[0]) +
                           self.k3 * (self.oldE1[0] + self.oldE1[2] - E[1] - self.oldE2[1]) -
                           self.k4 * self.oldE1[1]) - self.oldE2[2])

        self.oldE2[:] = self.oldE1[:]
        self.oldE1[:] = E[0: 3]


class ABCSecondRight(ABCSecondBase):
    def updateField(self, E, H):
        E[-1] = (self.k1 * (self.k2 * (E[-3] + self.oldE2[-1]) +
                            self.k3 * (self.oldE1[-1] + self.oldE1[-3] - E[-2] - self.oldE2[-2]) -
                            self.k4 * self.oldE1[-2]) - self.oldE2[-3])

        self.oldE2[:] = self.oldE1[:]
        self.oldE1[:] = E[-3:]
