%% Двумерный FDTD. Версия 1.0
% Поляризация TEz. Граничные условия - PEC
clear
clc

%% Параметры области моделирования
% Шаг сетки (d = dx = dy)
d = 1e-3;

% Время моделирования в секундах
maxTime_sec = 1.1e-9;

% Размер области моделирования в метрах
sizeX_m = 0.2;
sizeY_m = 0.2;

% Положение точечного источника в метрах
port_x_m = 0.1;
port_y_m = 0.1;

% Положение пробника в метрах
probe_x_m = 0.12;
probe_y_m = 0.08;

% Параметры гауссова сигнала
gauss_width_sec = 2e-11;
gauss_delay_sec = 2.5 * gauss_width_sec;

%% Физические константы
% Магнитная постоянная
mu0 = pi * 4e-7;

% Электрическая постоянная
eps0 = 8.854187817e-12;

% Скорость света в вакууме
c = 1.0 / sqrt (mu0 * eps0);


%% Расчет "дискретных" параметров моделирования
% "Одномерный" аналог числа Куранта для случая 2D
Cdtds = 1.0 / sqrt (2.0);

dt = d / c * Cdtds;

% Волновое сопротивление свободного пространства
W0 = 120 * pi;

% Время расчета в отсчетах
maxTime = ceil (maxTime_sec / dt);

% Размер области моделирования в отсчетах
sizeX = ceil (sizeX_m / d);
sizeY = ceil (sizeY_m / d);

% Положение точки возбуждения
port_x = ceil (port_x_m / d);
port_y = ceil (port_y_m / d);

% Положение пробника
probe_x = ceil(probe_x_m / d);
probe_y = ceil(probe_y_m / d);

gauss_width = gauss_width_sec / dt;
gauss_delay = gauss_delay_sec / dt;

%% Компоненты поля
Ex = zeros (sizeX - 1, sizeY);
Ey = zeros (sizeX, sizeY - 1);
Hz = zeros (sizeX - 1, sizeY - 1);


%% Параметры среды
% Диэлектрическая проницаемость среды
eps = ones (sizeX, sizeY);

% Магнитная проницаемость среды
mu = ones (sizeX, sizeY);

% Проводимость среды
sigma = zeros (sizeX, sizeY);

% "Магнитная проводимость" среды
sigma_m = zeros (sizeX, sizeY);

%% Коэффициенты для конечно-разностной схемы
loss_m = sigma_m .* dt ./ (2 * mu * mu0);
loss = sigma .* dt ./ (2 * eps * eps0);

Chzh = (1 - loss_m) ./ (1 + loss_m);

Chze = 1 ./ (1 + loss_m) .* (dt ./ (mu * mu0 * d));

Cexe = (1 - loss) ./ (1 + loss);

Cexh = 1 ./ (1 + loss) .* (dt ./ (eps * eps0 * d));

Ceye = Cexe;
Ceyh = Cexh;

% Какую компоненту поля будем отображать
visualize_field = Ey;

% Поле, зарегистрированное в датчике в зависимости от времени
probeTimeEx = zeros (1, maxTime);
probeTimeEy = zeros (1, maxTime);
probeTimeHz = zeros (1, maxTime);

%% Подготовка к визуализации двумерного поля
figure;
[x, y] = meshgrid (size(visualize_field, 1), size(visualize_field, 2));
x = x';
y = y';

%% Конечно-разностная схема
for t = 1: maxTime        
    for m = 1:sizeX - 1
        for n = 1:sizeY - 1
            Hz(m, n) = Chzh(m, n) * Hz(m, n) +...
                       Chze(m, n) * (Ex(m, n + 1) - Ex(m, n) -...
                                    (Ey(m + 1, n) - Ey(m, n)));
        end
    end

    for m = 1:sizeX - 1
        for n = 2:sizeY - 1
            Ex(m, n) = Cexe(m, n) * Ex(m, n) + ...
                       Cexh(m, n) * (Hz(m, n) - Hz(m, n - 1));
        end
    end

    for m = 2:sizeX - 1
        for n = 1:sizeY - 1
            Ey(m, n) = Ceye(m, n) * Ey(m, n) - ...
                       Ceyh(m, n) * (Hz(m, n) - Hz(m - 1, n));
        end
    end
    
    Hz(port_x, port_y) = Hz(port_x, port_y) +...
                         exp (-(t - gauss_delay) ^ 2 / (gauss_width ^ 2));
                     
    % Регистрация поля в пробнике
    probeTimeEx(t) = Ex(probe_x, probe_y);
    probeTimeEy(t) = Ey(probe_x, probe_y);
    probeTimeHz(t) = Hz(probe_x, probe_y);
    
    %surfl(x, y, Ex);
    %shading interp;

    imagesc(Ex', [-10, 10]);
    % colormap gray;
    colormap jet;
        
    zlim([-10, 10])
    
    hold on
    scatter(probe_x, probe_y, 100, 'x');
    scatter(port_x, port_y, 100, '*');
    hold off
    pause (0.03);
end

figure
subplot (3, 1, 1)
plot (probeTimeEx, 'b')
xlabel ('t, отсчет')
ylabel ('Ex, В/м')
grid on

subplot (3, 1, 2)
plot (probeTimeEy, 'b')
xlabel ('t, отсчет')
ylabel ('Ey, В/м')
grid on

subplot (3, 1, 3)
plot (probeTimeHz, 'r')
xlabel ('t, отсчет')
ylabel ('Hz, А/м')
grid on