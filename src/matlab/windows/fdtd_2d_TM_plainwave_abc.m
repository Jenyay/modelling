%% ��������� FDTD.
% ��������� ������� ABC ������ �������.
% ������� �����
clear
clc

%% ��������� ������� �������������
% ��� ����� (d = dx = dy)
d = 1e-3;

% ����� ������������� � ��������
maxTime_sec = 1e-9;

% ������ ������� ������������� � ������
sizeX_m = 0.2;
sizeY_m = 0.2;

% ��������� ��������� ������� �����
port_x_m = 0.1;

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

% ��������� ��������� ������� �����
port_x = ceil (port_x_m / d);

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

%% ������������ ��� ��������� �������.
% ���� �������, ��� � ��� �� ���� ������ ��������� ������������
temp1 = sqrt (Cezh(1, 1) .* Chye(1, 1));
temp2 = 1 ./ temp1 + 2 + temp1;

coef0 = -(1 ./ temp1 - 2 + temp1) ./ temp2;
coef1 = -2 * (temp1 - 1 ./ temp1) ./ temp2;
coef2 = 4 * (temp1 + 1 ./ temp1) ./ temp2;

% ����������� ���� ��� ��������� �������
% ������ ������ - ������ �� �������.
% ������ ������ - ������ �� ���������� X.
% ������ ������ - ������ �� ���������� Y.
EzLeft = zeros (2, 3, sizeY);
EzRight = zeros (2, 3, sizeY);
EzTop = zeros (2, sizeX, 3);
EzBottom = zeros (2, sizeX, 3);

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (1, maxTime);
probeTimeHx = zeros (1, maxTime);
probeTimeHy = zeros (1, maxTime);

figure;
[x, y] = meshgrid (1:sizeX, 1:sizeY);
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
    
    % ������������ ������� �����
    Ez(port_x, 2:end-1) = Ez(port_x, 2:end-1) +...
        exp (-(t - gauss_delay) ^ 2 / (gauss_width ^ 2));
    
    % �������������� ������� �����
    % Ez(2:end-1, port_x) = Ez(2:end-1, port_x) +...
    %    exp (-(t - gauss_delay) ^ 2 / (gauss_width ^ 2));
    
    % Ez(port_x, port_x) = Ez(port_x, port_x) +...
    %    exp (-(t - gauss_delay) ^ 2 / (gauss_width ^ 2));
    
    % ��������� ������� �����
    Ez(1, :) = coef0 .* (Ez(3, :) + squeeze (EzLeft(2, 1, :))') +...
        coef1 .* (squeeze (EzLeft(1, 1, :))' + squeeze(EzLeft(1, 3, :))' -...
            Ez(2, :) - squeeze(EzLeft(2, 2, :))') +...
        coef2 .* squeeze (EzLeft(1, 2, :))' - squeeze (EzLeft(2, 3, :))';
    
    % ��������� ������� ������
    Ez(end, :) = coef0 .* (Ez(end - 2, :) + squeeze(EzRight(2, 1, :))') +...
        coef1 .* (squeeze(EzRight(1, 1, :))' + squeeze(EzRight(1, 3, :))' -...
            Ez(end - 1, :) - squeeze(EzRight(2, 2, :))') +...
        coef2 .* squeeze(EzRight(1, 2, :))' - squeeze(EzRight(2, 3, :))';
    
    % ��������� ������� ������
    Ez(:, 1) = coef0 .* (Ez(:, 3) + squeeze (EzTop(2, :, 1))') +...
        coef1 .* (squeeze (EzTop(1, :, 1))' + squeeze (EzTop(1, :, 3))' -...
            Ez(:, 2) - squeeze (EzTop(2, :, 2))') +...
        coef2 .* squeeze (EzTop(1, :, 2))' - squeeze (EzTop(2, :, 3))';
    
    % ��������� ������� �����
    Ez(:, end) = coef0 .* (Ez(:, end - 2) + squeeze (EzBottom(2, :, 1))') +...
        coef1 .* (squeeze (EzBottom(1, :, 1))' + squeeze (EzBottom(1, :, 3))' -...
            Ez(:, end - 1) - squeeze (EzBottom(2, :, 2))') +...
        coef2 .* squeeze (EzBottom(1, :, 2))' - squeeze (EzBottom(2, :, 3))';
    
    % ���������� ����������� �����
    for n = 3:-1:2
        EzLeft (n, :, :) = EzLeft (n - 1, :, :);
        EzRight (n, :, :) = EzRight (n - 1, :, :);
        EzTop (n, :, :) = EzTop (n - 1, :, :);
        EzBottom (n, :, :) = EzBottom (n - 1, :, :);
    end
    
    for n = 1: 3
        EzLeft(1, n, :) = Ez(n, :);
        EzRight(1, n, :) = Ez(end - n + 1, :);
        EzTop(1, :, n) = Ez(:, n);
        EzBottom(1, :, n) = Ez(:, end - n + 1);
    end
    
    % ����������� ���� � ��������
    probeTimeEz(t) = Ez(probe_x, probe_y);
    probeTimeHx(t) = Hx(probe_x, probe_y);
    probeTimeHy(t) = Hy(probe_x, probe_y);
   
    %surfl(x, y, Ez);
    %shading interp;

    imagesc(Ez', [-1, 1]);
    colormap gray;
    
    hold on
    scatter(probe_x, probe_y, 100, 'wx');
    hold off
    zlim([-1.1, 1.1])
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