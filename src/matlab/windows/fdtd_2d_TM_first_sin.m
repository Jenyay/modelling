%% ��������� FDTD. ������ 1.0
% ����������� TMz. ��������� ������� - PEC
clear
clc

%% ��������� ������� �������������
% ��� ����� (d = dx = dy)
d = 1e-3;

% ����� ������������� � ��������
maxTime_sec = 1.1e-9 * 15;

% ������ ������� ������������� � ������
sizeX_m = 0.1;
sizeY_m = 0.1;

% ��������� ��������� ��������� � ������
port_x_m = sizeX_m / 2;
port_y_m = sizeY_m / 2;

% ��������� �������� � ������
probe_x_m = 0.05;
probe_y_m = sizeY_m / 3;

% ��������� �������� �������
gauss_width_sec = 2e-11;
gauss_delay_sec = 2.5 * gauss_width_sec;

Nl_m = 0.03;
Nl = Nl_m / d;

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
Hx = zeros (sizeX, sizeY - 1);
Hy = zeros (sizeX - 1, sizeY);
Ez = zeros (sizeX, sizeY);


%% ��������� �����
% ��������������� ������������� �����
eps = ones (sizeX, sizeY);

% ��������� ������������� �����
mu = ones (sizeX, sizeY);

% ������������ �����
sigma = zeros (sizeX, sizeY);

% "��������� ������������" �����
sigma_m = zeros (sizeX, sizeY);

phi_0 = -2 * pi / Nl;

%% ������������ ��� �������-���������� �����
Chxh = (1 - sigma_m .* dt ./ (2 * mu * mu0)) ./ ...
    (1 + sigma_m .* dt ./ (2 * mu * mu0));

Chxe = 1 ./ (1 + (sigma_m .* dt ./ (2 * mu * mu0))) .*...
    dt ./ (mu * mu0 * d);

Chyh = Chxh;

Chye = Chxe;

Ceze = (1 - sigma .* dt ./ (2 * eps * eps0)) ./ ...
    (1 + sigma .* dt ./ (2 * eps * eps0));

Cezh = 1 ./ (1 + (sigma .* dt ./ (2 * eps * eps0))) .*...
    dt ./ (eps * eps0 * d);

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (1, maxTime);
probeTimeHx = zeros (1, maxTime);
probeTimeHy = zeros (1, maxTime);

%% ���������� � ������������ ���������� ����
figure;
[x, y] = meshgrid (1:size(Ez, 1), 1:size(Ez, 2));
x = x';
y = y';

%% �������-���������� �����
for t = 1: maxTime        
    for m = 1:sizeX
        for n = 1:sizeY - 1
            Hx(m, n) = Chxh(m, n) * Hx(m, n) -...
                Chxe(m, n) * (Ez(m, n + 1) - Ez(m, n));
        end
    end

    for m = 1:sizeX - 1
        for n = 1:sizeY
            Hy(m, n) = Chyh(m, n) * Hy(m, n) +...
                Chye(m, n) * (Ez(m + 1, n) - Ez(m, n));
        end
    end

    for m = 2:sizeX - 1
        for n = 2:sizeY - 1
            Ez(m, n) = Ceze(m, n) * Ez(m, n) +...
                Cezh(m, n) * ((Hy(m, n) - Hy(m - 1, n)) -...
                (Hx(m, n) - Hx(m, n-1)));
        end
    end
    
    Ez(port_x, port_y) = Ez(port_x, port_y) +...
                         sin (2 * pi * t / Nl + phi_0);
                     
    % ����������� ���� � ��������
    probeTimeEz(t) = Ez(probe_x, probe_y);
    probeTimeHx(t) = Hx(probe_x, probe_y);
    probeTimeHy(t) = Hy(probe_x, probe_y);
    
    %surfl(x, y, Ez);
    %shading interp;

    % imagesc(Ez', [-0.1, 0.1]);
    imagesc([0, sizeX_m], [0, sizeY_m], Ez', [-0.5, 0.5]);
    %colormap gray;
    colormap jet;
    
    %zlim([-1, 1])
    
    hold on
    scatter(probe_x, probe_y, 100, 'x');
    scatter(port_x, port_y, 100, '*');
    hold off
    pause (0.01);
end

figure
subplot (3, 1, 1)
plot (probeTimeEz, 'b')
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on

subplot (3, 1, 2)
plot (probeTimeHx, 'r')
xlabel ('t, ������')
ylabel ('Hx, �/�')
grid on

subplot (3, 1, 3)
plot (probeTimeHy, 'r')
xlabel ('t, ������')
ylabel ('Hy, �/�')
grid on