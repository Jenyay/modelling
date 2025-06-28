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
    def getField(self, time):
        '''
        Метод должен возвращать значение поля источника в момент времени time
        '''
        pass


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

    def getField(self, time):
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

    def getField(self, time):
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

    def getField(self, time):
        return self.magnitude * np.sin(2 * np.pi * self.Sc * time / self.Nl) * np.exp(-((time - self.dg) / self.wg) ** 2)


class Harmonic(Source1D):
    '''
    Источник, создающий гармонический сигнал
    '''

    def __init__(self, magnitude, Nl, Sc, phi_0=None):
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

    def getField(self, time):
        return self.magnitude * np.sin(2 * np.pi * self.Sc * time / self.Nl + self.phi_0)


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

    def getField(self, time):
        t = (np.pi ** 2) * (self.Sc * time / self.Nl - self.Md) ** 2
        return self.magnitude * (1 - 2 * t) * np.exp(-t)
