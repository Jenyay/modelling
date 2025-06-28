# -*- coding: utf-8 -*-
'''
Двумерный FDTD. Поляризация TMz. Граничные условия - PEC.
Источник возбуждения - цилиндрическая волна.
'''

import matplotlib.pyplot as plt

import numpy as np


if __name__ == '__main__':
    # Шаг сетки в метрах (d = dx = dy)
    d = 1e-3

    # Время моделирования в секундах
    maxTime_sec = 1.1e-9

    # Размер области моделирования в метрах
    sizeX_m = 0.3
    sizeY_m = 0.2

    # Положение точечного источника в метрах
    port_x_m = 0.15
    port_y_m = 0.1

    # Положение датчика в метрах
    probe_x_m = 0.12
    probe_y_m = 0.08

    # Параметры гауссова сигнала
    gauss_width_sec = 2e-11
    gauss_delay_sec = 2.5 * gauss_width_sec

    # Физические константы
    # Магнитная постоянная
    mu0 = np.pi * 4e-7

    # Электрическая постоянная
    eps0 = 8.854187817e-12

    # Скорость света в вакууме
    c = 1.0 / np.sqrt(mu0 * eps0)

    # Расчет "дискретных" параметров моделирования
    Cdtds = 1.0 / np.sqrt(2.0)

    dt = d / c * Cdtds

    # Волновое сопротивление свободного пространства
    W0 = 120 * np.pi

    # Время расчета в отсчетах
    maxTime = int(np.ceil(maxTime_sec / dt))

    # Размер области моделирования в отсчетах
    sizeX = int(np.ceil(sizeX_m / d))
    sizeY = int(np.ceil(sizeY_m / d))

    # Положение точки возбуждения в отсчетах
    port_x = int(np.ceil(port_x_m / d))
    port_y = int(np.ceil(port_y_m / d))

    # Положение датчика в отсчетах
    probe_x = int(np.ceil(probe_x_m / d))
    probe_y = int(np.ceil(probe_y_m / d))

    gauss_width = gauss_width_sec / dt
    gauss_delay = gauss_delay_sec / dt

    # Компоненты поля
    Hx = np.zeros((sizeX, sizeY))
    Hy = np.zeros((sizeX, sizeY))
    Ez = np.zeros((sizeX, sizeY))

    # Параметры среды
    # Диэлектрическая проницаемость среды
    eps = np.ones((sizeX, sizeY))

    # Магнитная проницаемость среды
    mu = np.ones((sizeX, sizeY))

    # Проводимость среды
    sigma = np.zeros((sizeX, sizeY))

    # "Магнитная проводимость" среды
    sigma_m = np.zeros((sizeX, sizeY))

    # Коэффициенты для конечно-разностной схемы
    loss_m = sigma_m * dt / (2 * mu * mu0)
    loss = sigma * dt / (2 * eps * eps0)

    Chxh = ((1 - sigma_m * dt / (2 * mu * mu0)) /
            (1 + sigma_m * dt / (2 * mu * mu0)))

    Chxe = 1 / (1 + (sigma_m * dt / (2 * mu * mu0))) * dt / (mu * mu0 * d)

    Chyh = Chxh
    Chye = Chxe

    Ceze = ((1 - sigma * dt / (2 * eps * eps0)) /
            (1 + sigma * dt / (2 * eps * eps0)))

    Cezh = (1 / (1 + (sigma * dt / (2 * eps * eps0))) *
            dt / (eps * eps0 * d))

    # Какую компоненту поля будем отображать
    visualize_field = Ez

    # Поле, зарегистрированное в датчике в зависимости от времени
    probeTimeHx = np.zeros(maxTime)
    probeTimeHy = np.zeros(maxTime)
    probeTimeEz = np.zeros(maxTime)

    plt.ion()
    fig = plt.figure()

    for q in range(1, maxTime):
        Hx[:, :-1] = (Chxh[:, :-1] * Hx[:, :-1] -
                      Chxe[:, :-1] * (Ez[:, 1:] - Ez[:, :-1]))

        Hy[:-1, :] = (Chyh[:-1, :] * Hy[:-1, :] +
                      Chye[:-1, :] * (Ez[1:, :] - Ez[:-1, :]))

        Ez[1:-1, 1:-1] = (Ceze[1:-1, 1:-1] * Ez[1:-1, 1:-1] +
                          Cezh[1:-1, 1:-1] * ((Hy[1:-1, 1:-1] - Hy[:-2, 1:-1]) -
                                              (Hx[1:-1, 1:-1] - Hx[1:-1, :-2])))

        Ez[port_x, port_y] += np.exp(-(q - gauss_delay) ** 2 / (gauss_width ** 2))

        probeTimeHx[q] = Hx[probe_x, probe_y]
        probeTimeHy[q] = Hy[probe_x, probe_y]
        probeTimeEz[q] = Ez[probe_x, probe_y]

        if q % 2 == 0:
            plt.clf()
            plt.imshow(visualize_field.transpose(),
                       vmin=-0.05,
                       vmax=0.05,
                       cmap='jet')
            plt.scatter([probe_x], [probe_y], marker='x')
            plt.draw()
            plt.pause(0.01)

    plt.ioff()
    plt.figure()

    plt.subplot(3, 1, 1)
    plt.plot(probeTimeEz, 'r')
    plt.xlabel('q, отсчет')
    plt.ylabel('Ez, В/м')
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.plot(probeTimeHx, 'b')
    plt.xlabel('q, отсчет')
    plt.ylabel('Hx, А/м')
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.plot(probeTimeHy, 'b')
    plt.xlabel('q, отсчет')
    plt.ylabel('Hy, А/м')
    plt.grid()

    plt.show()
