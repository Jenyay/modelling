%% Одномерный FDTD. Версия 1.6.1
% Граница раздела воздух - диэлектрик.
% На правой границе массива расположен диэлектрик с потерями.
% Добавлено усреднение коэффициентов для расчета затухания на границе
% поглощающего слоя.
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Время расчета в отсчетах
maxTime = 750;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение источника
sourcePos = 50;

% Положение датчика, регистрирующего поля
probePos = 60;

% Начало диэлектрического слоя
layer_x = 100;

% Где начинается поглощающий диэлектрик
layer_loss_x = 160;

% Потери в среде. loss = sigma * dt / (2 * eps * eps0)
loss = zeros(1, maxSize);
loss(layer_loss_x: end) = 0.01;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

% Коэффициенты для расчета поля E
ceze = (1 - loss) ./ (1 + loss);
cezh = W0 ./ (eps .* (1 + loss));

% Усреднение коэффициентов на границе поглощающего слоя
ceze(layer_loss_x) = (ceze(layer_loss_x - 1) +...
    ceze(layer_loss_x + 1)) / 2;
cezh(layer_loss_x) = (cezh(layer_loss_x - 1) +...
    cezh(layer_loss_x + 1)) / 2;

% Коэффициенты для расчета поля H
chyh = (1 - loss) ./ (1 + loss);
chye = 1 ./ (W0 * (1 + loss));

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = chyh(m) * Hy(m) + ...
            chye(m) * (Ez(m + 1) - Ez(m));
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) - ...
        exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % Расчет компоненты поля E
    Ez(1) = Ez(2);
    
    for m = 2: maxSize - 1
        % До этой строки Ez(n) хранит значение компоненты EzS
        % за предыдущий момент времени
        % Вместо W0 / eps используется cezh
        Ez(m) = ceze(m) * Ez(m) + ...
            cezh(m) * (Hy(m) - Hy(m - 1));
    end

    % Источник возбуждения
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 30.0) ^ 2 / 100.0);
    
    % Регистрация поля в точке
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, отсчет')
    ylabel ('Ez, В/м')
    line ([layer_x, layer_x], [-1.1, 1.1], ...
        'Color',[0.0, 0.0, 0.0]);
    line ([layer_loss_x, layer_loss_x], [-1.1, 1.1], ...
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