%% Одномерный FDTD. Версия 1.5
% Среда с потерями.
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Время расчета в отсчетах
maxTime = 450;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение источника
sourcePos = 50;

% Положение датчиков, регистрирующих поля, в отсчетах
probePos = [110, 130, 150, 170];

% Начало слоя с потерями
layer_x = 100;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

% Потери в среде. loss = sigma * dt / (2 * eps * eps0)
loss = zeros (1, maxSize);
loss(layer_x: end) = 0.01;

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

ceze = (1 - loss) ./ (1 + loss);
cezh = W0 ./ (eps .* (1 + loss));

% Поля, зарегистрированное в датчиках в зависимости от времени
% Первый индекс - номер датчика,
% второй индекс - временной отсчет.
probeTimeEz = zeros(size(probePos, 2), maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0;
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1)...
        - exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % Расчет компоненты поля E
    % Т.е. пока справа простейшее граничное условие и так не работает,
    % правое граничное условие убрано.
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
    
    % Регистрация поля в датчиках
    for p = 1:size(probePos, 2)
        probeTimeEz(p, t) = Ez(probePos(p));
    end;
    
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