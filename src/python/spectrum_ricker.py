# -*- coding: utf-8 -*-
'''
Расчет спектра вейвлета Рикера
'''

import matplotlib.pyplot as plt

import numpy as np
from numpy.fft import fft, fftshift


if __name__ == '__main__':
    # Размер массива
    size = 1024

    # шаг по времени
    dt = 0.4e-10

    # Параметры вейвлета Рикера
    fp = 1e9
    Md = 1.7
    dr = Md / fp

    # Шаг по частоте
    df = 1.0 / (size * dt)

    # Вейвлет Рикера
    time = np.arange(0, size * dt, dt)
    impulse = ((1 - 2 * (np.pi * fp * (time - dr)) ** 2) *
               np.exp(-(np.pi * fp * (time - dr)) ** 2))

    # Расчет спектра
    spectrum = np.abs(fft(impulse))
    spectrum = fftshift(spectrum)

    # Расчет частоты
    freq = np.arange(-size / 2 * df, size / 2 * df, df)

    # Отображение импульса
    plt.subplot(1, 2, 1)
    plt.plot(time, impulse)
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
