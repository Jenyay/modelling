%% ���������� FDTD. ������ 1.0.3
% ����� �� ������������ �������� �� �������� � ���������.
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� �������
Sc = 1.0;

% ����� ������� � ��������
maxTime = 1000;

% ������ ������� ������������� � ��������
maxSize = 200;

% ��������� �������, ��������������� ����
probePos = 50;

Ez = zeros (1, maxSize);
Hy = zeros (size (Ez));

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    Hy(1:end-1) = Hy(1:end-1) +...
        (Ez(2:end) - Ez(1:end-1)) * Sc / W0;
    
    % ������ ���������� ���� E
    Ez(2:end) = Ez(2:end) +...
        (Hy(2:end) - Hy(1:end-1)) * Sc * W0;
    
    % �������� �����������
    Ez(1) = exp (-(t - 30.0) ^ 2 / 100.0);
    
    % ����������� ���� � �����
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
    grid on
    
    pause (0.03)
end

figure
plot (probeTimeEz)
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on