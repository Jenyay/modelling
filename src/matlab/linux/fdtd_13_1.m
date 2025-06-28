%% Одномерный FDTD. Версия 1.9.1
% Граница раздела. Используются граничные условия ABC второго порядка.
% Все параметры заданы в метрах и секундах
clear
clc

% ********************
% Исходные данные
% Размер сетки
dx = 1 * 1e-3;

% Размер области моделирования в метрах
maxSize_m = 0.4;

% Время моделирования в секундах
maxTime_sec = 3e-9;

% Начало второго слоя в метрах
layer_x_m = 0.2;

% Положения датчиков, регистрирующего поля, в метрах
probePos_m = [0.05, 0.15, 0.25, 0.30];

% Положение точки возбуждения в метрах
port_x_m = 0.1;

% Параметры гауссова сигнала
gauss_width_sec = 3e-11;
gauss_delay_sec = 3 * gauss_width_sec;

% ********************

% Расчет "дискретных" параметров
% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Скорость света в вакууме
c = 299792458;

% Число Куранта
Sc = 1.0;

% Временной шаг в секундах
dt = Sc * dx / c;

% Время расчета в отсчетах
maxTime = ceil (maxTime_sec / dt);

% Размер области моделирования в отсчетах
maxSize = maxSize_m / dx;

% Положение датчиков, регистрирующего поля
probePos = ceil (probePos_m / dx);

% Количество датчиков
probeCount = size (probePos, 2);

% Начало диэлектрического слоя
layer_x = ceil (layer_x_m / dx);

% Положение точки возбуждения
port_x = ceil (port_x_m / dx);

gauss_width = gauss_width_sec / dt;
gauss_delay = gauss_delay_sec / dt;

fprintf ('dx = %.3f мм;\n', dx * 1e3);
fprintf ('dt = %e с;\n', dt);
fprintf ('Число Куранта: %.3f;\n', Sc);
fprintf ('Область моделирования: %.3f м (%d ячеек);\n', maxSize_m, maxSize);
fprintf ('Время моделирования: %.e с (%d отсчетов);\n', maxTime_sec, maxTime);
fprintf ('Положение второго слоя: %.3f м (%d ячеек);\n', layer_x_m, layer_x);
fprintf ('Положение точки возбуждения: %.3f м (%d ячеек);\n', port_x_m, port_x);
fprintf ('Положения датчиков:\n');
for probe=1:probeCount
    fprintf ('    %d. %.3f м (%d ячеек);\n',...
        probe, probePos_m(probe), probePos(probe));
end

fprintf ('Коэффициент ширины гауссова импульса: %e сек (%d отсчетов);\n',...
    gauss_width_sec, gauss_width);
fprintf ('Задержка гауссова импульса: %e сек (%d отсчетов);\n',...
    gauss_delay_sec, gauss_delay);

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

mu = ones (size (Ez));

% !!! Коэффициенты для расчета ABC второй степени на левой границе

% Sc' для левой границы
Sc1Left = Sc / sqrt (mu(1) * eps(1));

k1Left = -1 / (1 / Sc1Left + 2 + Sc1Left);
k2Left = 1 / Sc1Left - 2 + Sc1Left;
k3Left = 2 * (Sc1Left - 1 / Sc1Left);
k4Left = 4 * (1 / Sc1Left + Sc1Left);

% Sc' для правой границы
Sc1Right = Sc / sqrt (mu(end) * eps(end));

k1Right = -1 / (1 / Sc1Right + 2 + Sc1Right);
k2Right = 1 / Sc1Right - 2 + Sc1Right;
k3Right = 2 * (Sc1Right - 1 / Sc1Right);
k4Right = 4 * (1 / Sc1Right + Sc1Right);

% Ez(1), Ez(2), Ez(3) в предыдущий момент времени (q)
oldEzLeft1 = zeros(3);
oldEzRight1 = zeros(3);

% Ez(1), Ez(2), Ez(3) в пред-предыдущий момент времени (q-1)
oldEzLeft2 = zeros(3);
oldEzRight2 = zeros(3);


% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (probeCount, maxTime);
probe_y = zeros (size (probePos));

x_m = (1:maxSize) * dx;

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0 / mu(m);
    end
    
    Hy(port_x-1) = Hy(port_x-1) -...
        exp (-(t - gauss_delay) ^ 2 / (gauss_width ^ 2)) / W0;
    
    % Расчет компоненты поля E
  
    for m = 2: maxSize - 1
        % До этой строки Ez(n) хранит значение компоненты EzS
        % за предыдущий момент времени
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * W0 / eps (m);
    end

    % Источник возбуждения
    Ez(port_x) = Ez(port_x) +...
        exp (-(t + 0.5 - (-0.5) - gauss_delay) ^ 2 / (gauss_width ^ 2));
    
    % !!!
    % Граничные условия ABC второй степени (слева)
    Ez(1) = k1Left * (k2Left * (Ez(3) + oldEzLeft2(1)) +...
        k3Left * (oldEzLeft1(1) + oldEzLeft1(3) - Ez(2) - oldEzLeft2(2)) - ...
        k4Left * oldEzLeft1(2)) - oldEzLeft2(3);
    
    oldEzLeft2 = oldEzLeft1;
    oldEzLeft1 = Ez(1:3);
    
    % Граничные условия ABC второй степени (справа)
    Ez(end) = k1Right * (k2Right * (Ez(end - 2) + oldEzRight2(end)) +...
        k3Right * (oldEzRight1(end) + oldEzRight1(end - 2) - Ez(end - 1) - oldEzRight2(end - 1)) - ...
        k4Right * oldEzRight1(end - 1)) - oldEzRight2(end - 2);
    
    oldEzRight2 = oldEzRight1;
    oldEzRight1 = Ez(end-2: end);
    
    
    % Регистрация поля в точке
    for probe=1:probeCount
        probeTimeEz(probe, t) = Ez(probePos(probe));
    end
    
    plot (x_m, Ez, '-b', probePos_m, probe_y, 'kx');
    xlim ([0, maxSize_m]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, мм')
    ylabel ('Ez, В/м')
    line ([layer_x_m, layer_x_m], [-1.1, 1.1], ...
        'Color',[0.0, 0.0, 0.0]);
    pause (0.01)
end

figure
hold on

probeLegend = {zeros(probeCount)};
for probe=1:probeCount
    probeLegend(probe) = cellstr (sprintf ('x = %.3f mm', ...
        probePos_m(probe) * dx * 1e3));
end

time = (1:maxTime) * dt;
for probe=1:probeCount
    plot (time, probeTimeEz(probe, :))
end

xlabel ('t, с')
ylabel ('Ez, В/м')
legend (probeLegend);
grid on
hold off