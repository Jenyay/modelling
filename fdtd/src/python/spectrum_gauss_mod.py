# -*- coding: utf-8 -*-
'''
Расчет спектра модулированного гауссова импульса
'''

import matplotlib.pyplot as plt

import numpy as np
from numpy.fft import fft, fftshift


if __name__ == '__main__':
    # Размер массива
    size = 1024

    # шаг по времени
    dt = 0.2e-10

    # Параметры модулированного гауссова сигнала
    A_0 = 100
    A_max = 100
    f_0 = 5e9
    DeltaF = 4e9

    # Шаг по частоте
    df = 1.0 / (size * dt)

    w_g = 2 * np.sqrt(np.log(A_max)) / (np.pi * DeltaF)
    d_g = w_g * np.sqrt(np.log(A_0))

    # Гауссов импульс
    time = np.arange(0, size * dt, dt)
    gauss = np.sin(2 * np.pi * f_0 * time) * np.exp(-((time - d_g) / w_g) ** 2)

    # Расчет спектра
    spectrum = np.abs(fft(gauss))
    spectrum = fftshift(spectrum)

    # Расчет частоты
    freq = np.arange(-size / 2 * df, size / 2 * df, df)

    # Отображение импульса
    plt.subplot(1, 2, 1)
    plt.plot(time, gauss)
    plt.xlim(0, 0.4e-8)
    plt.grid()
    plt.xlabel('Время, с')
    plt.ylabel('Ez')

    # Отображение спектра
    plt.subplot(1, 2, 2)
    plt.plot(freq, spectrum / np.max(spectrum))
    plt.grid()
    plt.xlabel('Частота, Гц')
    plt.ylabel('|S| / |Smax|')
    plt.xlim(0, 10e9)

    plt.subplots_adjust(wspace=0.3)
    plt.show()
