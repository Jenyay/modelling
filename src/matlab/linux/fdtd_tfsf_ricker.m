%% Одномерный FDTD. Версия 1.7.1
% Источник возбуждения в виде вейвлета Рикера.
% Используется метод TFSF.
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Время расчета в отсчетах
maxTime = 300;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение датчика, регистрирующего поля
probePos = 50;

% Положение источника возбуждения
sourcePos = 50;

Sc = 1.0;
Np = 30;
Md = 2.5;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0;
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) - ...
        (1 - 2 * pi ^ 2 * (Sc * t / Np - Md) ^ 2) *...
        exp (-pi ^ 2 * (Sc * t / Np - Md) ^ 2) / W0;
    
    % Расчет компоненты поля E
    Ez(1) = Ez(2);
    Ez(end) = Ez(end - 1);
    
    for m = 2: maxSize - 1
        % До этой строки Ez(n) хранит значение компоненты EzS
        % за предыдущий момент времени
        % Вместо W0 / eps используется cezh
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * W0;
    end

    % Источник возбуждения
    Ez(sourcePos) = Ez(sourcePos) +...
        (1 - 2 * pi ^ 2 * ((Sc * (t + 0.5) - (-0.5)) / Np - Md) ^ 2) *...
        exp (-pi ^ 2 * ((Sc * (t + 0.5) - (-0.5)) / Np - Md) ^ 2);
    
    % Регистрация поля в точке
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, отсчет')
    ylabel ('Ez, В/м')
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