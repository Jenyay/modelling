%% Одномерный FDTD.
% Граница раздела
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Число Куранта
Sc = 1.0;

% Время расчета в отсчетах
maxTime = 600;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение датчиков, регистрирующих поля, в отсчетах
probePos = [60, 110, 160];

% Положение источника возбуждения в отсчетах
sourcePos = 50;

% Положение начала диэлектрика
layer_x = 100;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize);

eps = ones (1, maxSize);
eps(layer_x: end) = 9.0;

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
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) -...
        exp (-(t - 30.0) ^ 2 / 100.0) * Sc / W0;
    
    % Расчет компоненты поля E
    Ez(1) = Ez(2);
    for m = 2: maxSize
        % До этой строки Ez(n) хранит значение компоненты Ez
        % за предыдущий момент времени
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * Sc * W0 / eps (m);
    end

    % Источник возбуждения
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 30.0) ^ 2 / 100.0) * Sc;
    
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
    plot (sourcePos, 0, '*r');
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
