%% Одномерный FDTD.
% Отображение компонент поля E и H
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

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
probeTimeHy = zeros (1, maxTime);

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
    probeTimeEz(t) = Ez(probePos);
    probeTimeHy(t) = Hy(probePos);
    
    subplot (2, 1, 1)
    plot (Ez, 'b');
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, отсчет')
    ylabel ('Ez, В/м')
    grid on
    hold on
    plot (probePos, 0, 'xk');
    hold off
    
    subplot (2, 1, 2)
    plot (Hy, 'r');
    xlim ([1, maxSize]);
    ylim ([-1.1 / 377, 1.1 / 377]);
    xlabel ('x, отсчет')
    ylabel ('Hy, А/м')
    grid on
    hold on
    plot (probePos, 0, 'xk');
    hold off
    
    pause (0.03)
end

figure
subplot (2, 1, 1)
plot (probeTimeEz, 'b')
xlabel ('t, отсчет')
ylabel ('Ez, В/м')
grid on

subplot (2, 1, 2)
plot (probeTimeHy, 'r')
xlabel ('t, отсчет')
ylabel ('Hy, А/м')
grid on