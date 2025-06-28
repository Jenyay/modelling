%% ���������� FDTD.
% ������� �������
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� �������
Sc = 1.0;

% ����� ������� � ��������
maxTime = 1000;

% ������ ������� ������������� � ��������
maxSize = 250;

% ��������� ��������, �������������� ����, � ��������
probePos = [60, 110, 160];

% ����� ������� TFSF
tfsf_left = 50;

% ������ ������� TFSF
tfsf_right = 200;

% ��������� ������ �����������
layer_start = 100;
layer_end = 150;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize);

eps = ones (1, maxSize);
eps(layer_start: layer_end) = 9.0;

mu = ones (1, maxSize);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    Hy(maxSize) = Hy(maxSize - 1);
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(n) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) * Sc / (W0 * mu(m));
    end
    
    Hy(tfsf_left - 1) = Hy(tfsf_left - 1) - ...
        exp (-(t - 30.0 - (tfsf_left - tfsf_left)) ^ 2 / 100.0) / W0;

    Hy(tfsf_right - 1) = Hy(tfsf_right - 1) + ...
        exp (-(t - 30.0 - (tfsf_right - tfsf_left)) ^ 2 / 100.0) / W0;
    
    % ������ ���������� ���� E
    Ez(1) = Ez(2);

    for m = 2: maxSize
        % �� ���� ������ Ez(n) ������ �������� ���������� Ez
        % �� ���������� ������ �������
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * Sc * W0 / eps (m);
    end

    % �������� �����������
    Ez(tfsf_left) = Ez(tfsf_left) + ...
        exp (-(t + 0.5 - (tfsf_left - tfsf_left - 0.5) - 30.0) ^ 2 / 100.0);
    
    Ez(tfsf_right) = Ez(tfsf_right) - ...
        exp (-(t + 0.5 - (tfsf_right - tfsf_left - 0.5) - 30.0) ^ 2 / 100.0);
    
    % ����������� ���� � ��������
    for p = 1:size(probePos, 2)
        probeTimeEz(p, t) = Ez(probePos(p));
    end
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
    line ([layer_start, layer_start], [-1.1, 1.1], ...
        'Color',[0.0, 0.0, 0.0]);
    line ([layer_end, layer_end], [-1.1, 1.1], ...
        'Color',[0.0, 0.0, 0.0]);
    grid on
    hold on
    plot (tfsf_left, 0, '*r');
    plot (tfsf_right, 0, '*r')
    hold off
    pause (0.03)
end
