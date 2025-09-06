# -*- coding: utf-8 -*-
'''
Моделирование распространения ЭМ волны, падающей на границу
вакуум - идеальный диэлектрик.
Используются граничные условия ABC второй степени.
'''

import matplotlib.pyplot as plt

import numpy as np
from numpy.fft import fft

import tools


if __name__ == '__main__':
    # Характеристическое сопротивление свободного пространства
    Z0 = 120.0 * np.pi

    c = 299792458.0

    # Число Куранта
    Sc = 0.9

    # Время расчета в отсчетах
    maxTime = 800

    # Размер области моделирования в отсчетах
    maxSize = 600

    # Положение источника в отсчетах
    sourcePos = 50

    # Положения датчиков
    probe1Pos = 100
    probe2Pos = 300

    # Расстояние между датчиками
    probeDist = probe2Pos - probe1Pos

    # Датчики для регистрации поля
    probesPos = [probe1Pos, probe2Pos]
    probes = [tools.Probe(pos, maxTime) for pos in probesPos]

    # Параметры среды
    # Диэлектрическая проницаемость
    eps = np.ones(maxSize)

    # Магнитная проницаемость
    mu = np.ones(maxSize - 1)

    Ez = np.zeros(maxSize)
    Hy = np.zeros(maxSize - 1)

    # Коэффициенты для расчета ABC второй степени
    # Sc' для левой границы
    Sc1Left = Sc / np.sqrt(mu[0] * eps[0])

    k1Left = -1 / (1 / Sc1Left + 2 + Sc1Left)
    k2Left = 1 / Sc1Left - 2 + Sc1Left
    k3Left = 2 * (Sc1Left - 1 / Sc1Left)
    k4Left = 4 * (1 / Sc1Left + Sc1Left)

    # Sc' для правой границы
    Sc1Right = Sc / np.sqrt(mu[-1] * eps[-1])

    k1Right = -1 / (1 / Sc1Right + 2 + Sc1Right)
    k2Right = 1 / Sc1Right - 2 + Sc1Right
    k3Right = 2 * (Sc1Right - 1 / Sc1Right)
    k4Right = 4 * (1 / Sc1Right + Sc1Right)

    # Ez[0: 2] в предыдущий момент времени (q)
    oldEzLeft1 = np.zeros(3)

    # Ez[0: 2] в пред-предыдущий момент времени (q - 1)
    oldEzLeft2 = np.zeros(3)

    # Ez[-3: -1] в предыдущий момент времени (q)
    oldEzRight1 = np.zeros(3)

    # Ez[-3: -1] в пред-предыдущий момент времени (q - 1)
    oldEzRight2 = np.zeros(3)

    # Параметры отображения поля E
    display_field = Ez
    display_ylabel = 'Ez, В/м'
    display_ymin = -1.1
    display_ymax = 1.1

    # Создание экземпляра класса для отображения
    # распределения поля в пространстве
    display = tools.AnimateFieldDisplay(maxSize,
                                        display_ymin, display_ymax,
                                        display_ylabel)

    display.activate()
    display.drawProbes(probesPos)
    display.drawSources([sourcePos])

    # Номер индекса в спектре, в котором считаем, что фаза меняется линейно
    k_index = 10

    for q in range(maxTime):
        # Расчет компоненты поля H
        Hy = Hy + (Ez[1:] - Ez[:-1]) * Sc / (Z0 * mu)

        # Расчет компоненты поля E
        Ez[1:-1] = Ez[1: -1] + (Hy[1:] - Hy[: -1]) * Sc * Z0 / eps[1: -1]

        Ez[sourcePos] += np.exp(-(q - 0.5 - 30.0) ** 2 / 9.0)

        # Граничные условия ABC второй степени (слева)
        Ez[0] = (k1Left * (k2Left * (Ez[2] + oldEzLeft2[0]) +
                           k3Left * (oldEzLeft1[0] + oldEzLeft1[2] - Ez[1] - oldEzLeft2[1]) -
                           k4Left * oldEzLeft1[1]) - oldEzLeft2[2])

        oldEzLeft2[:] = oldEzLeft1[:]
        oldEzLeft1[:] = Ez[0: 3]

        # Граничные условия ABC второй степени (справа)
        Ez[-1] = (k1Right * (k2Right * (Ez[-3] + oldEzRight2[-1]) +
                             k3Right * (oldEzRight1[-1] + oldEzRight1[-3] - Ez[-2] - oldEzRight2[-2]) -
                             k4Right * oldEzRight1[-2]) - oldEzRight2[-3])

        oldEzRight2[:] = oldEzRight1[:]
        oldEzRight1[:] = Ez[-3:]

        # Регистрация поля в датчиках
        for probe in probes:
            probe.addData(Ez, Hy)

        if q % 2 == 0:
            display.updateData(display_field, q)

    display.stop()

    # Отображение сигналов и их спектров, зарегистрированных в датчиках
    plt.figure()
    plt.suptitle('Сигналы в датчиках')

    for n, probe in enumerate(probes):
        EzField = probe.E
        spectrum = fft(EzField)
        spectrum_abs = np.abs(spectrum)
        spectrum_phase = np.unwrap(np.angle(spectrum))

        # Расчет фазы с вычтенным линейным членом
        k = spectrum_phase[k_index] / k_index
        spectrum_phase_line = (spectrum_phase -
                               k * np.arange(0, len(spectrum_phase)))

        # Отображение сигнала в датчике
        plt.subplot(4, 1, 1)
        plt.plot(EzField, label='датчик N {}'.format(n + 1))
        plt.xlabel('q, отсчет')
        plt.ylabel('Ez, В/м')
        plt.grid(True)
        plt.legend()

        # Амплитудный спектр сигнала в датчике
        plt.subplot(4, 1, 2)
        plt.plot(spectrum_abs, label='датчик N {}'.format(n + 1))
        plt.xlabel('f, отсчет')
        plt.ylabel('|Ez|, В/(м*Гц)')
        plt.xlim(0, 300)
        plt.grid(True)
        plt.legend()

        # Фазовый спектр сигнала в датчике без вычитания линейного члена
        plt.subplot(4, 1, 3)
        plt.plot(spectrum_phase, label='датчик N {}'.format(n + 1))
        plt.xlabel('f, отсчет')
        plt.ylabel('Phase(Ez), рад.')
        plt.xlim(0, 300)
        plt.grid(True)
        plt.legend()

        # Фазовый спектр сигнала в датчике
        plt.subplot(4, 1, 4)
        plt.plot(spectrum_phase_line, label='датчик N {}'.format(n + 1))
        plt.xlabel('f, отсчет')
        plt.ylabel('Phase(Ez), рад.')
        plt.xlim(0, 300)
        plt.ylim(-5, 5)
        plt.grid(True)
        plt.legend()

    # Сигнал и спектр в первом датчике
    EzField_0 = probes[0].E
    spectrum_0 = fft(EzField_0)
    spectrum_0_phase = np.unwrap(np.angle(spectrum_0))

    # Сигнал и спектр во втором датчике
    EzField_1 = probes[1].E
    spectrum_1 = fft(EzField_1)
    spectrum_1_phase = np.unwrap(np.angle(spectrum_1))

    phase_delta = np.abs(spectrum_1_phase - spectrum_0_phase)

    # Коэффициент прохождения среды между двумя датчиками
    R = spectrum_1 / spectrum_0
    R_abs = np.abs(R)
    R_phase = np.unwrap(np.angle(R))

    # Вычитание линейного члена из фазы коэффициента прохождения
    k = R_phase[k_index] / k_index
    R_phase_line = R_phase - k * np.arange(0, len(R))

    plt.figure()
    plt.suptitle('Коэффициент прохождения')

    # Отображение спектра падающего сигнала
    plt.subplot(3, 1, 1)
    plt.plot(np.abs(spectrum_0))
    plt.xlabel('f, отсчет')
    plt.ylabel('|Ez|, В/(м*Гц)')
    plt.xlim(0, 300)
    plt.grid()

    # Отображение амплитуды коэффициента прохождения
    plt.subplot(3, 1, 2)
    plt.plot(R_abs)
    plt.xlabel('f, отсчет')
    plt.ylabel('|R|')
    plt.xlim(0, 300)
    plt.ylim(0, 1.1)
    plt.grid()

    # Отображение фазы коэффициента прохождения
    plt.subplot(3, 1, 3)
    plt.plot(R_phase_line)
    plt.xlabel('f, отсчет')
    plt.ylabel('Phase(R), рад.')
    plt.xlim(0, 300)
    plt.ylim(-4, 4)
    plt.grid()

    # Расчет фазовой скорости на каждой частоте
    v = (c * probeDist * 2 * np.pi *
         np.arange(0, len(spectrum_0)) / (Sc * phase_delta * len(EzField_1)))

    # Отображение спектра падающего сигнала
    plt.figure()
    plt.suptitle('Фазовая скорость')
    plt.subplot(2, 1, 1)
    plt.plot(np.abs(spectrum_0))
    plt.xlabel('f, отсчет')
    plt.ylabel('|Ez|, В/(м*Гц)')
    plt.xlim(0, 300)
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(v / c)
    plt.xlabel('f, отсчет')
    plt.ylabel('v / c')
    plt.xlim(0, 300)
    plt.ylim(0.9, 1.1)
    plt.grid()

    plt.show()
