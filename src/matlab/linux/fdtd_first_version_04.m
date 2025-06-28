%% Одномерный FDTD. Версия 1.0.3
% Циклы по пространству заменены на операции с матрицами.
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Число Куранта
Sc = 1.0;

% Время расчета в отсчетах
maxTime = 1000;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение датчика, регистрирующего поля
probePos = 50;

Ez = zeros (1, maxSize);
Hy = zeros (size (Ez));

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    Hy(1:end-1) = Hy(1:end-1) +...
        (Ez(2:end) - Ez(1:end-1)) * Sc / W0;
    
    % Расчет компоненты поля E
    Ez(2:end) = Ez(2:end) +...
        (Hy(2:end) - Hy(1:end-1)) * Sc * W0;
    
    % Источник возбуждения
    Ez(1) = exp (-(t - 30.0) ^ 2 / 100.0);
    
    % Регистрация поля в точке
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, отсчет')
    ylabel ('Ez, В/м')
    grid on
    
    pause (0.03)
end

figure
plot (probeTimeEz)
xlabel ('t, отсчет')
ylabel ('Ez, В/м')
grid on