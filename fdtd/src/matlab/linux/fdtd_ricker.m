%% Одномерный FDTD. Версия 1.7
% Источник возбуждения в виде вейвлета Рикера.
% Без использования метода TFSF.
clear

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Потери в среде. loss = sigma * dt / (2 * eps * eps0)
loss = 0.02;

% Где начинается поглощающий диэлектрик
layer_loss_x = 180;

% Время расчета в отсчетах
maxTime = 550;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение датчика, регистрирующего поля
probePos = 50;

layer_x = 100;

Sc = 1;
Np = 30;
Md = 2;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

% Коэффициенты для расчета поля E
ceze = ones (1, maxSize);
ceze(layer_loss_x: end) = (1 - loss) / (1 + loss);

cezh = (ones (1, maxSize) * W0 ./ eps);
cezh(layer_loss_x: end) = cezh(layer_loss_x: end) / (1 + loss);

% Коэффициенты для расчета поля H
chyh = ones (1, maxSize - 1);
chyh(layer_loss_x: end) = (1 - loss) / (1 + loss);

chye = ones (1, maxSize - 1) / W0;
chye(layer_loss_x: end) = chye(layer_loss_x: end) / (1 + loss);

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = chyh(m) * Hy(m) +...
            chye(m) * (Ez(m + 1) - Ez(m));
    end
    
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
    Ez(50) = Ez(50) +...
        (1 - 2 * pi ^ 2 * (Sc * t / Np - Md) ^ 2) *...
        exp (-pi ^ 2 * (Sc * t / Np - Md) ^ 2);
    
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
    pause (0.03)
end

figure
plot (probeTimeEz)
xlabel ('t, отсчет')
ylabel ('Ez, В/м')
grid on