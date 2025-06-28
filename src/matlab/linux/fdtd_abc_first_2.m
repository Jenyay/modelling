%% Одномерный FDTD.
% Граница раздела. 
% Используются граничные условия ABC первого порядка.
% Циклы по пространству заменены на операции с матрицами.
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Число Куранта
Sc = 1;

% Время расчета в отсчетах
maxTime = 750;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение датчика, регистрирующего поля
probePos = 160;

% Начало диэлектрического слоя
layer_x = 100;

% Положение источника.
sourcePos = 50;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

mu = ones (size (Ez));

% !!!
% Ez(2) в предыдущий момент времени
oldEzLeft = 0;

% !!!
% Ez(end-1) в предыдущий момент времени
oldEzRight = 0;

% !!!
% Расчет коэффициентов для граничных условий
tempLeft = Sc / sqrt (mu(1) * eps(1));
koeffABCLeft = (tempLeft - 1) / (tempLeft + 1);

tempRight = Sc / sqrt (mu(end) * eps(end));
koeffABCRight = (tempRight - 1) / (tempRight + 1);

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    Hy(1:end) = Hy(1:end) +...
        (Ez(2:end) - Ez(1:end-1)) / W0 ./ mu(1:end-1);
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) -...
        exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % Расчет компоненты поля E
    Ez(2:end-1) = Ez(2:end-1) +...
        (Hy(2:end) - Hy(1:end-1)) * W0 ./ eps (2:end-1);
    
    % Источник возбуждения
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 30.0) ^ 2 / 100.0);
    
    % Граничные условия ABC первой степени
    Ez(1) = oldEzLeft + koeffABCLeft * (Ez(2) - Ez(1));
    oldEzLeft = Ez(2);
    
    Ez(end) = oldEzRight + koeffABCRight * (Ez(end-1) - Ez(end));
    oldEzRight = Ez(end-1);
    
    % Регистрация поля в точке
    probeTimeEz(t) = Ez(probePos);
    
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
plot (probeTimeEz)
xlabel ('t, отсчет')
ylabel ('Ez, В/м')
grid on