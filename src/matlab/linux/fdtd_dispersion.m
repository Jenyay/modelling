%% Гауссов импульс распространяется в свободном пространстве с Sc < 1
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Время расчета в отсчетах
maxTime = 1024;

% Размер области моделирования в отсчетах
maxSize = 2000;

% Положение датчика, регистрирующего поля
probePos = 1500;

% Положение источника возбуждения
sourcePos = 1200;

Sc = 0.5;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize);

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) * Sc / W0;
    end
    
    % Расчет компоненты поля E
    for m = 2: maxSize
        % До этой строки Ez(n) хранит значение компоненты EzS
        % за предыдущий момент времени
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * Sc * W0;
    end

    % Источник возбуждения
    Ez(sourcePos) = Ez(sourcePos) + exp (-(t - 50.0) ^ 2 / 50.0) * Sc;
    
    % Регистрация поля в точке
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1000, 1600]);
    ylim ([-1.0, 1.0]);
    xlabel ('x, отсчет')
    ylabel ('Ez, В/м')
    grid on
    hold on
    plot (probePos, 0, 'xk');
    plot (sourcePos, 0, '*r');
    hold off
    pause (0.01)
end

spectrum = fft(probeTimeEz);
spectrum_abs = abs(spectrum);
spectrum_phase = unwrap(angle(spectrum));

figure
% Сигнал в датчике
subplot(3, 1, 1)
plot (probeTimeEz)
xlabel ('t, отсчет')
ylabel ('Ez, В/м')
grid on

% Амплитудный спектр сигнала в датчике
subplot(3, 1, 2)
plot (spectrum_abs)
xlabel ('f')
ylabel ('|Ez|, В/(м*Гц)')
xlim([0, 300])
grid on

% Фазовый спектр сигнала в датчике
subplot(3, 1, 3)
plot (spectrum_phase)
xlabel ('f')
ylabel ('Phase(Ez), рад.')
xlim([0, 300])
grid on
