# -*- coding: utf-8 -*-
'''
Расчет спектра гауссова импульса
'''

import matplotlib.pyplot as plt

import numpy as np
from numpy.fft import fft, fftshift


if __name__ == '__main__':
    # Размер массива
    size = 1024

    # шаг по времени
    dt = 0.4e-10

    # Параметры гауссова сигнала
    A_0 = 100
    A_max = 100
    F_max = 3e9

    # Шаг по частоте
    df = 1.0 / (size * dt)

    w_g = np.sqrt(np.log(A_max)) / (np.pi * F_max)
    d_g = w_g * np.sqrt(np.log(A_0))

    print(f'w_g = {w_g:.5e}')
    print(f'd_g = {d_g:.5e}')

    # Гауссов импульс
    time = np.arange(0, size * dt, dt)
    gauss = np.exp(-((time - d_g) / w_g) ** 2)

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
    plt.xlim(0, 5e9)

    plt.subplots_adjust(wspace=0.4)
    plt.show()
