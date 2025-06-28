# -*- coding: utf-8 -*-
'''
Модуль с классами источников разного типа
'''

from abc import ABCMeta, abstractmethod

import numpy as np


class Source1D(metaclass=ABCMeta):
    '''
    Базовый класс для всех источников одномерного метода FDTD
    '''
    @abstractmethod
    def getE(self, time):
        '''
        Метод должен возвращать значение поля источника в момент времени time
        '''
        pass

    def getH(self, time):
        return 0.0


class SourcePlaneWave(metaclass=ABCMeta):
    @abstractmethod
    def getE(self, position, time):
        pass


class SourceTFSF(Source1D):
    def __init__(self, source: SourcePlaneWave,
                 sourcePos: float,
                 Sc: float = 1.0,
                 eps: float = 1.0,
                 mu: float = 1.0):
        self.source = source
        self.sourcePos = sourcePos
        self.Sc = Sc
        self.eps = eps
        self.mu = mu
        self.W0 = 120.0 * np.pi

    def getH(self, time):
        return -(self.Sc / (self.W0 * self.mu)) * self.source.getE(self.sourcePos, time)

    def getE(self, time):
        return (self.Sc / np.sqrt(self.eps * self.mu)) * self.source.getE(self.sourcePos - 0.5, time + 0.5)


class Gaussian(Source1D):
    '''
    Источник, создающий гауссов импульс
    '''

    def __init__(self, magnitude, dg, wg):
        '''
        magnitude - максимальное значение в источнике;
        dg - коэффициент, задающий начальную задержку гауссова импульса;
        wg - коэффициент, задающий ширину гауссова импульса.
        '''
        self.magnitude = magnitude
        self.dg = dg
        self.wg = wg

    def getE(self, time):
        return self.magnitude * np.exp(-((time - self.dg) / self.wg) ** 2)


class GaussianDiff(Source1D):
    '''
    Источник, создающий дифференцированный гауссов импульс
    '''

    def __init__(self, magnitude, dg, wg):
        '''
        magnitude - максимальное значение в источнике;
        dg - коэффициент, задающий начальную задержку гауссова импульса;
        wg - коэффициент, задающий ширину гауссова импульса.
        '''
        self.magnitude = magnitude
        self.dg = dg
        self.wg = wg

    def getE(self, time):
        e = (time - self.dg) / self.wg
        return -2 * self.magnitude * e * np.exp(-(e ** 2))


class GaussianMod(Source1D):
    '''
    Источник, создающий модулированный гауссов импульс
    '''

    def __init__(self, magnitude, dg, wg, Nl, Sc):
        '''
        magnitude - максимальное значение в источнике;
        dg - коэффициент, задающий начальную задержку гауссова импульса;
        wg - коэффициент, задающий ширину гауссова импульса;
        Nl - количество отсчетов на длину волны;
        Sc - число Куранта.
        '''
        self.magnitude = magnitude
        self.dg = dg
        self.wg = wg
        self.Nl = Nl
        self.Sc = Sc

    def getE(self, time):
        return self.magnitude * np.sin(2 * np.pi * self.Sc * time / self.Nl) * np.exp(-((time - self.dg) / self.wg) ** 2)


class Harmonic(Source1D):
    '''
    Источник, создающий гармонический сигнал
    '''

    def __init__(self, magnitude, Nl, phi_0=None, Sc=1.0):
        '''
        magnitude - максимальное значение в источнике;
        Nl - количество отсчетов на длину волны;
        Sc - число Куранта.
        '''
        self.magnitude = magnitude
        self.Nl = Nl
        self.Sc = Sc

        if phi_0 is None:
            self.phi_0 = -2 * np.pi / Nl
        else:
            self.phi_0 = phi_0

    def getE(self, time):
        return self.magnitude * np.sin(2 * np.pi * self.Sc * time / self.Nl + self.phi_0)

    @staticmethod
    def make_continuous(magnitude: float,
                        freq: float,
                        dt: float,
                        Sc: float) -> 'Harmonic':
        # Количество ячеек на длину волны
        Nl = Sc / (freq * dt)
        phi_0 = -2 * np.pi / Nl
        return Harmonic(magnitude, Nl, phi_0, Sc)


class HarmonicPlaneWave(SourcePlaneWave):
    ''' Класс с уравнением плоской волны для гармонического сигнала в дискретном виде
    magnitude - амплитуда сигнала
    Nl - количество ячеек на длину волны.
    phi0 - начальная фаза.
    Sc - число Куранта.
    eps - относительная диэлектрическая проницаемость среды, в которой расположен источник.
    mu - относительная магнитная проницаемость среды, в которой расположен источник.
    '''

    def __init__(self, magnitude, Nl, phi0, Sc=1.0, eps=1.0, mu=1.0):
        self.magnitude = magnitude
        self.Nl = Nl
        self.phi0 = phi0
        self.Sc = Sc
        self.eps = eps
        self.mu = mu

    def getE(self, m, q):
        '''
        Расчет поля E в дискретной точке пространства m
        в дискретный момент времени q
        '''
        return self.magnitude * np.sin(2 * np.pi / self.Nl * (self.Sc * q - np.sqrt(self.mu * self.eps) * m) + self.phi0)

    @staticmethod
    def make_continuous(magnitude: float,
                        freq: float,
                        dt: float,
                        Sc: float,
                        eps: float = 1.0,
                        mu: float = 1.0) -> 'HarmonicPlaneWave':
        # Количество ячеек на длину волны
        Nl = Sc / (freq * dt)
        phi_0 = -2 * np.pi / Nl
        return HarmonicPlaneWave(magnitude, Nl, phi_0, Sc)


class Ricker(Source1D):
    '''
    Источник, создающий импульс в форме вейвлета Рикера
    '''

    def __init__(self, magnitude, Nl, Md, Sc):
        '''
        magnitude - максимальное значение в источнике;
        Nl - количество отсчетов на длину волны;
        Md - определяет задержку импульса;
        Sc - число Куранта.
        '''
        self.magnitude = magnitude
        self.Nl = Nl
        self.Md = Md
        self.Sc = Sc

    def getE(self, time):
        t = (np.pi ** 2) * (self.Sc * time / self.Nl - self.Md) ** 2
        return self.magnitude * (1 - 2 * t) * np.exp(-t)
