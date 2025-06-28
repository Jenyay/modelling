%% ��������� FDTD. ������ 1.0
% ����������� TEz. ��������� ������� - PEC
clear
clc

%% ��������� ������� �������������
% ��� ����� (d = dx = dy)
d = 1e-3;

% ����� ������������� � ��������
maxTime_sec = 1.1e-9;

% ������ ������� ������������� � ������
sizeX_m = 0.2;
sizeY_m = 0.2;

% ��������� ��������� ��������� � ������
port_x_m = 0.1;
port_y_m = 0.1;

% ��������� �������� � ������
probe_x_m = 0.12;
probe_y_m = 0.08;

% ��������� �������� �������
gauss_width_sec = 2e-11;
gauss_delay_sec = 2.5 * gauss_width_sec;

%% ���������� ���������
% ��������� ����������
mu0 = pi * 4e-7;

% ������������� ����������
eps0 = 8.854187817e-12;

% �������� ����� � �������
c = 1.0 / sqrt (mu0 * eps0);


%% ������ "����������" ���������� �������������
% "����������" ������ ����� ������� ��� ������ 2D
Cdtds = 1.0 / sqrt (2.0);

dt = d / c * Cdtds;

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� ������� � ��������
maxTime = ceil (maxTime_sec / dt);

% ������ ������� ������������� � ��������
sizeX = ceil (sizeX_m / d);
sizeY = ceil (sizeY_m / d);

% ��������� ����� �����������
port_x = ceil (port_x_m / d);
port_y = ceil (port_y_m / d);

% ��������� ��������
probe_x = ceil(probe_x_m / d);
probe_y = ceil(probe_y_m / d);

gauss_width = gauss_width_sec / dt;
gauss_delay = gauss_delay_sec / dt;

%% ���������� ����
Ex = zeros (sizeX - 1, sizeY);
Ey = zeros (sizeX, sizeY - 1);
Hz = zeros (sizeX - 1, sizeY - 1);


%% ��������� �����
% ��������������� ������������� �����
eps = ones (sizeX, sizeY);

% ��������� ������������� �����
mu = ones (sizeX, sizeY);

% ������������ �����
sigma = zeros (sizeX, sizeY);

% "��������� ������������" �����
sigma_m = zeros (sizeX, sizeY);

%% ������������ ��� �������-���������� �����
loss_m = sigma_m .* dt ./ (2 * mu * mu0);
loss = sigma .* dt ./ (2 * eps * eps0);

Chzh = (1 - loss_m) ./ (1 + loss_m);

Chze = 1 ./ (1 + loss_m) .* (dt ./ (mu * mu0 * d));

Cexe = (1 - loss) ./ (1 + loss);

Cexh = 1 ./ (1 + loss) .* (dt ./ (eps * eps0 * d));

Ceye = Cexe;
Ceyh = Cexh;

% ����� ���������� ���� ����� ����������
visualize_field = Ey;

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEx = zeros (1, maxTime);
probeTimeEy = zeros (1, maxTime);
probeTimeHz = zeros (1, maxTime);

%% ���������� � ������������ ���������� ����
figure;
[x, y] = meshgrid (size(visualize_field, 1), size(visualize_field, 2));
x = x';
y = y';

%% �������-���������� �����
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
                     
    % ����������� ���� � ��������
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
xlabel ('t, ������')
ylabel ('Ex, �/�')
grid on

subplot (3, 1, 2)
plot (probeTimeEy, 'b')
xlabel ('t, ������')
ylabel ('Ey, �/�')
grid on

subplot (3, 1, 3)
plot (probeTimeHz, 'r')
xlabel ('t, ������')
ylabel ('Hz, �/�')
grid on