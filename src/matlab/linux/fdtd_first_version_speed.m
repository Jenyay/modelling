%% Одномерный FDTD.
% Расчет скорости распространения волны
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Время расчета в отсчетах
maxTime = 250;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение датчика, регистрирующего поля
probePos_1 = 50;
probePos_2 = 150;

Ez = zeros (1, maxSize);
Hy = zeros (size (Ez));

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz_1 = zeros (1, maxTime);
probeTimeEz_2 = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0;
    end
    
    % Расчет компоненты поля E
    for m = 2: maxSize
        % До этой строки Ez(n) хранит значение компоненты Ez
        % за предыдущий момент времени
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * W0;
    end

    % Источник возбуждения
    Ez(1) = exp (-(t - 30.0) ^ 2 / 100.0);
    
    % Регистрация поля в точке
    probeTimeEz_1(t) = Ez(probePos_1);
    probeTimeEz_2(t) = Ez(probePos_2);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, отсчет')
    ylabel ('Ez, В/м')
    grid on
    
    hold on
    plot (probePos_1, 0, 'xk');
    plot (probePos_2, 0, 'xk');
    hold off
    
    pause (0.03)
end

figure
hold on
plot (probeTimeEz_1, 'b')
plot (probeTimeEz_2, 'r')
hold off
xlabel ('t, отсчет')
ylabel ('Ez, В/м')
grid on