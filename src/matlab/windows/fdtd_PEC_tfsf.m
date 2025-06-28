%% Одномерный FDTD.
% Граница раздела
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Число Куранта
Sc = 1.0;

% Время расчета в отсчетах
maxTime = 500;

% Размер области моделирования в отсчетах
maxSize = 250;

% Положение датчиков, регистрирующих поля, в отсчетах
probePos = [60];

% Левая граница TFSF
tfsf_left = 50;

% Правая граница TFSF
tfsf_right = 150;

% Положение металлической плоскости (PEC)
layer_x = 100;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize);

eps = ones (1, maxSize);
mu = ones (1, maxSize);

% Поля, зарегистрированное в датчиках в зависимости от времени
% Первый индекс - номер датчика,
% второй индекс - временной отсчет.
probeTimeEz = zeros (size(probePos, 2), maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    Hy(maxSize) = Hy(maxSize - 1);
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) * Sc / (W0 * mu(m));
    end
    
    Hy(tfsf_left - 1) = Hy(tfsf_left - 1) - ...
        exp (-(t - 30.0 - (tfsf_left - tfsf_left)) ^ 2 / 100.0) / W0;

    Hy(tfsf_right - 1) = Hy(tfsf_right - 1) + ...
        exp (-(t - 30.0 - (tfsf_right - tfsf_left)) ^ 2 / 100.0) / W0;
    
    % Расчет компоненты поля E
    Ez(1) = Ez(2);
    
    for m = 2: maxSize
        % До этой строки Ez(n) хранит значение компоненты Ez
        % за предыдущий момент времени
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * Sc * W0 / eps (m);
    end

    % Источник возбуждения
    Ez(tfsf_left) = Ez(tfsf_left) + ...
        exp (-(t + 0.5 - (tfsf_left - tfsf_left - 0.5) - 30.0) ^ 2 / 100.0);
    
    Ez(tfsf_right) = Ez(tfsf_right) - ...
        exp (-(t + 0.5 - (tfsf_right - tfsf_left - 0.5) - 30.0) ^ 2 / 100.0);
    
    Ez(layer_x) = 0;
    
    % Регистрация поля в датчиках
    for p = 1:size(probePos, 2)
        probeTimeEz(p, t) = Ez(probePos(p));
    end
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, отсчет')
    ylabel ('Ez, В/м')
    line ([layer_x, layer_x], [-1.1, 1.1], ...
        'Color',[0.0, 0.0, 0.0]);
    grid on
    hold on
    plot (probePos, 0, 'xk');
    plot (tfsf_left, 0, '*r');
    plot (tfsf_right, 0, '*r')
    hold off
    pause (0.03)
end

figure
hold on
for p = 1:size(probePos, 2)
    plot (probeTimeEz(p,:))
end
hold off
xlabel ('t, отсчет')
ylabel ('Ez, В/м')
grid on
