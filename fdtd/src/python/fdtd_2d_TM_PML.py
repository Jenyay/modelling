# -*- coding: utf-8 -*-
'''
Двумерный FDTD
Поляризация - TMz.
Источник возбуждения - точечный гармонический.
Граничные условия - PML.
'''

import matplotlib.pyplot as plt

import numpy


if __name__ == '__main__':
    # Физические константы
    # Магнитная постоянная
    mu0 = numpy.pi * 4e-7

    # Электрическая постоянная
    eps0 = 8.854187817e-12

    # Скорость света в вакууме
    c = 1.0 / numpy.sqrt(mu0 * eps0)

    # Шаг сетки (d = dx = dy)
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

    # Частота источника
    f = 5e9
    wavelength_m = c / f
    wavelength = wavelength_m / d
    phi_0 = -2 * numpy.pi / wavelength

    # Параметры PML
    # Толщина слоя PML в отсчетах
    PML_h = 10

    # Потери в слое PML
    PML_loss = 0.05

    # Расчет "дискретных" параметров моделирования
    # "Одномерный" аналог числа Куранта для случая 2D
    Cdtds = 1.0 / numpy.sqrt(2.0)

    dt = d / c * Cdtds

    # Волновое сопротивление свободного пространства
    W0 = 120 * numpy.pi

    # Время расчета в отсчетах
    maxTime = int(numpy.ceil(maxTime_sec / dt))

    # Размер области моделирования в отсчетах
    sizeX = int(numpy.ceil(sizeX_m / d))
    sizeY = int(numpy.ceil(sizeY_m / d))

    # Положение точки возбуждения
    port_x = int(numpy.ceil(port_x_m / d))
    port_y = int(numpy.ceil(port_y_m / d))

    # Положение датчика
    probe_x = int(numpy.ceil(probe_x_m / d))
    probe_y = int(numpy.ceil(probe_y_m / d))

    # Компоненты поля
    Hx = numpy.zeros((sizeX, sizeY))
    Hy = numpy.zeros((sizeX, sizeY))
    Ez = numpy.zeros((sizeX, sizeY))

    # Параметры среды
    # Диэлектрическая проницаемость среды
    eps = numpy.ones((sizeX, sizeY))

    # Магнитная проницаемость среды
    mu = numpy.ones((sizeX, sizeY))

    # Проводимость среды
    sigma = numpy.zeros((sizeX, sizeY))

    # "Магнитная проводимость" среды
    sigma_m = numpy.zeros((sizeX, sizeY))

    # Коэффициенты для конечно-разностной схемы
    loss_m = sigma_m * dt / (2 * mu * mu0)
    loss = sigma * dt / (2 * eps * eps0)

    # Потери для PML
    loss[:PML_h, :] = PML_loss
    loss_m[:PML_h, :] = PML_loss
    loss[-PML_h - 1:, :] = PML_loss
    loss_m[-PML_h - 1:, :] = PML_loss

    loss[:, :PML_h] = PML_loss
    loss_m[:, :PML_h] = PML_loss
    loss[:, -PML_h - 1:] = PML_loss
    loss_m[:, -PML_h - 1:] = PML_loss

    # Расчет коэффициентов для FDTD
    Chxh = ((1 - loss_m) / (1 + loss_m))
    Chxe = 1 / (1 + loss_m) * dt / (mu * mu0 * d)

    Chyh = Chxh
    Chye = Chxe

    Ceze = ((1 - loss) / (1 + loss))
    Cezh = (1 / (1 + loss) * dt / (eps * eps0 * d))

    # Усреднение границ PML
    for cxxx in [Chxh, Chxe, Chyh, Chye, Ceze, Cezh]:
        cxxx[PML_h, :] = (cxxx[PML_h - 1, :] + cxxx[PML_h + 1, :]) / 2
        cxxx[-PML_h - 1, :] = (cxxx[-PML_h - 2, :] + cxxx[-PML_h, :]) / 2
        cxxx[:, PML_h] = (cxxx[:, PML_h - 1] + cxxx[:, PML_h + 1]) / 2
        cxxx[:, -PML_h - 1] = (cxxx[:, -PML_h - 2] + cxxx[:, -PML_h]) / 2

    # Какую компоненту поля будем отображать
    visualize_field = Ez

    # Поле, зарегистрированное в датчике в зависимости от времени
    probeTimeHx = numpy.zeros(maxTime)
    probeTimeHy = numpy.zeros(maxTime)
    probeTimeEz = numpy.zeros(maxTime)

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

        Ez[port_x, port_y] += numpy.sin(2 * numpy.pi * q / wavelength + phi_0)

        probeTimeHx[q] = Hx[probe_x, probe_y]
        probeTimeHy[q] = Hy[probe_x, probe_y]
        probeTimeEz[q] = Ez[probe_x, probe_y]

        if q % 2 == 0:
            plt.clf()
            plt.imshow(visualize_field.transpose(),
                       vmin=-0.1,
                       vmax=0.1,
                       cmap='jet')
            plt.scatter([probe_x], [probe_y], marker='x')
            plt.draw()
            plt.pause(0.01)

    plt.ioff()
    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(probeTimeHx, 'b')
    plt.xlabel('q, отсчет')
    plt.ylabel('Hx, А/м')
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.plot(probeTimeHy, 'b')
    plt.xlabel('q, отсчет')
    plt.ylabel('Hy, А/м')
    plt.grid()

    plt.subplot(3, 1, 3)
    plt.plot(probeTimeEz, 'r')
    plt.xlabel('q, отсчет')
    plt.ylabel('Ez, В/м')
    plt.grid()

    plt.show()
