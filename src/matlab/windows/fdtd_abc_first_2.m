%% ���������� FDTD.
% ������� �������. 
% ������������ ��������� ������� ABC ������� �������.
% ����� �� ������������ �������� �� �������� � ���������.
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� �������
Sc = 1;

% ����� ������� � ��������
maxTime = 750;

% ������ ������� ������������� � ��������
maxSize = 200;

% ��������� �������, ��������������� ����
probePos = 160;

% ������ ���������������� ����
layer_x = 100;

% ��������� ���������.
sourcePos = 50;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

mu = ones (size (Ez));

% !!!
% Ez(2) � ���������� ������ �������
oldEzLeft = 0;

% !!!
% Ez(end-1) � ���������� ������ �������
oldEzRight = 0;

% !!!
% ������ ������������� ��� ��������� �������
tempLeft = Sc / sqrt (mu(1) * eps(1));
koeffABCLeft = (tempLeft - 1) / (tempLeft + 1);

tempRight = Sc / sqrt (mu(end) * eps(end));
koeffABCRight = (tempRight - 1) / (tempRight + 1);

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    Hy(1:end) = Hy(1:end) +...
        (Ez(2:end) - Ez(1:end-1)) / W0 ./ mu(1:end-1);
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) -...
        exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % ������ ���������� ���� E
    Ez(2:end-1) = Ez(2:end-1) +...
        (Hy(2:end) - Hy(1:end-1)) * W0 ./ eps (2:end-1);
    
    % �������� �����������
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 30.0) ^ 2 / 100.0);
    
    % ��������� ������� ABC ������ �������
    Ez(1) = oldEzLeft + koeffABCLeft * (Ez(2) - Ez(1));
    oldEzLeft = Ez(2);
    
    Ez(end) = oldEzRight + koeffABCRight * (Ez(end-1) - Ez(end));
    oldEzRight = Ez(end-1);
    
    % ����������� ���� � �����
    probeTimeEz(t) = Ez(probePos);
    
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
plot (probeTimeEz)
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on