%% Одномерный FDTD. Версия 1.9
% Граница раздела. 
% Используются граничные условия ABC второй степени.

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Число Куранта
Sc = 1;

% Время расчета в отсчетах
maxTime = 750;

% Размер области моделирования в отсчетах
maxSize = 200;

% Положение источника.
sourcePos = 50;

% Положение датчика, регистрирующего поле
probePos = 160;

layer_x = 100;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

mu = ones (size (Ez));

% !!! Коэффициенты для расчета ABC второй степени
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

% Ez(1:3) в предыдущий момент времени (q)
oldEzLeft1 = zeros(3);

% Ez(1:3) в пред-предыдущий момент времени (q-1)
oldEzLeft2 = zeros(3);

% Ez(end-2: end) в предыдущий момент времени (q)
oldEzRight1 = zeros(3);

% Ez(end-2: end) в пред-предыдущий момент времени (q-1)
oldEzRight2 = zeros(3);

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % Расчет компоненты поля H
    for m = 1: maxSize - 1
        % До этой строки Hy(n) хранит значение компоненты Hy
        % за предыдущий момент времени
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0 / mu(m);
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) -...
        exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % Расчет компоненты поля E
  
    for m = 2: maxSize - 1
        % До этой строки Ez(n) хранит значение компоненты EzS
        % за предыдущий момент времени
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * W0 / eps (m);
    end

    % Источник возбуждения
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 30.0) ^ 2 / 100.0);
    
    % !!!
    % Граничные условия ABC второй степени (слева)
    Ez(1) = k1Left * (k2Left * (Ez(3) + oldEzLeft2(1)) +...
        k3Left * (oldEzLeft1(1) + oldEzLeft1(3) - Ez(2) - oldEzLeft2(2)) - ...
        k4Left * oldEzLeft1(2)) - oldEzLeft2(3);
    
    oldEzLeft2 = oldEzLeft1;
    oldEzLeft1 = Ez(1:3);
    
    % Граничные условия ABC второй степени (справа)
    Ez(end) = k1Right * (k2Right * (Ez(end - 2) + oldEzRight2(end)) +...
        k3Right * (oldEzRight1(end) + oldEzRight1(end - 2) - Ez(end - 1)...
        - oldEzRight2(end - 1)) - ...
        k4Right * oldEzRight1(end - 1)) - oldEzRight2(end - 2);
    
    oldEzRight2 = oldEzRight1;
    oldEzRight1 = Ez(end-2: end);
    
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