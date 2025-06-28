%% ���������� FDTD.
% ������� �������
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� �������
Sc = 1.0;

% ����� ������� � ��������
maxTime = 600;

% ������ ������� ������������� � ��������
maxSize = 200;

% ��������� ��������, �������������� ����, � ��������
probePos = [60, 110, 160];

% ��������� ��������� ����������� � ��������
sourcePos = 50;

% ��������� ������ �����������
layer_x = 100;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize);

eps = ones (1, maxSize);
eps(layer_x: end) = 9.0;

mu = ones (1, maxSize);

% ����, ������������������ � �������� � ����������� �� �������
% ������ ������ - ����� �������,
% ������ ������ - ��������� ������.
probeTimeEz = zeros (size(probePos, 2), maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    Hy(maxSize) = Hy(maxSize - 1);
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(n) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) * Sc / (W0 * mu(m));
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) -...
        exp (-(t - 30.0) ^ 2 / 100.0) * Sc / W0;
    
    % ������ ���������� ���� E
    Ez(1) = Ez(2);
    for m = 2: maxSize
        % �� ���� ������ Ez(n) ������ �������� ���������� Ez
        % �� ���������� ������ �������
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * Sc * W0 / eps (m);
    end

    % �������� �����������
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 30.0) ^ 2 / 100.0) * Sc;
    
    % ����������� ���� � ��������
    for p = 1:size(probePos, 2)
        probeTimeEz(p, t) = Ez(probePos(p));
    end
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
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
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on
