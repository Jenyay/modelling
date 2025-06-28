%% Одномерный FDTD. Версия 1.3.1
% Синусоидальный сигнал распространяется в одну сторону (TFSF boundary)
% Источник находится в диэлектрике
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Число Куранта
Sc = 1;

% Время расчета в отсчетах
maxTime = 500;

% Размер области моделирования в отсчетах
maxSize = 200;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize);

eps = ones (size (Ez));
eps(1: end) = 9.0;

mu = ones (size (Ez));
%mu(1: end) = 4.0;

% Положение датчика, регистрирующего поля
probePos = 60;

% Положение источника возбуждения
sourcePos = 50;

% Параметры гармонического сигнала
Nl = 60;
phi_0 = -2 * pi / Nl;
%phi_0 = 0;

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / (W0 * mu(m)) * Sc;
    end
    
    % Источник возбуждения с использованием метода 
    % Total Field / Scattered Field
    Hy(sourcePos - 1) = Hy(sourcePos - 1) - ...
        Sc / (W0 * mu(sourcePos - 1)) * ...
        sin(2 * pi * t * Sc / Nl + phi_0);
    
    % Расчет компоненты поля E
    for m = 2: maxSize
        % До этой строки Ez(n) хранит значение компоненты EzS
        % за предыдущий момент времени
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * (W0 / eps(m)) * Sc;
    end

    % Источник возбуждения с использованием метода 
    % Total Field / Scattered Field
    Ez(sourcePos) = Ez(sourcePos) + ...
      Sc / (sqrt(eps(sourcePos) * mu(sourcePos))) *...
      sin(2 * pi / Nl * ((t + 0.5) * Sc - (-0.5 * sqrt(eps(sourcePos) * mu(sourcePos)))) + phi_0);
    
    % Регистрация поля в точке
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, отсчет')
    ylabel ('Ez, В/м')
    title (sprintf('%d', t))
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