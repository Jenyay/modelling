%% ���������� FDTD. ������ 1.4.1
% ������� �������. Hy ����� �� ���� ������ ������.
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

% ��������� ��������� �����������
sourcePos = 50;

% ��������� ������ �����������
layer_x = 100;
% layer_x2 = 120;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;
% eps(layer_x2: end) = 4.0;

mu = ones (size (Hy));

% ����, ������������������ � �������� � ����������� �� �������
% ������ ������ - ����� �������,
% ������ ������ - ��������� ������.
probeTimeEz = zeros (size(probePos, 2), maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(m) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) * Sc / W0 / mu(m);
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) -...
        exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % ������ ���������� ���� E
    Ez(1) = Ez(2);
    Ez(maxSize) = Ez(maxSize - 1);
    
    for m = 2: maxSize - 1
        % �� ���� ������ Ez(m) ������ �������� ���������� Ez
        % �� ���������� ������ �������
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * Sc * W0 / eps (m);
    end

    % �������� �����������
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 30.0) ^ 2 / 100.0);
    
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
    % line ([layer_x2, layer_x2], [-1.1, 1.1], ...
    %     'Color',[0.0, 0.0, 0.0]);
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