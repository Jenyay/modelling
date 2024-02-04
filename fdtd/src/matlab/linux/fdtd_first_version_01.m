%% Одномерный FDTD. Версия 1.0
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

% Начальные условия
Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize);

% Значение компонент поля в предыдущий момент времени
% Ez(q - 1), Hy(q - 1/2)
Ez_prev = zeros (size (Ez));
Hy_prev = zeros (size (Hy));

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

for t = 1: maxTime
    Ez_prev = Ez;
    Hy_prev = Hy;
    
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        Hy(m) = Hy_prev(m) + (Ez_prev(m + 1) - Ez_prev(m)) * Sc / W0;
    end

    % Расчет компоненты поля E
    for m = 2: maxSize
        Ez(m) = Ez_prev(m) + (Hy(m) - Hy(m - 1)) * Sc * W0;
    end

    % Источник возбуждения
    Ez(1) = exp (-(t - 30.0) ^ 2 / 100.0);

    % Регистрация поля в точке
    probeTimeEz(t) = Ez(probePos);
end

figure
plot (probeTimeEz)
xlabel ('t, отсчет')
ylabel ('Ez, В/м')
grid on
