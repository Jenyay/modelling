%% ���������� FDTD. ������ 1.0.1
% ��������� ��������
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

% ��������� �������
Ez = zeros (1, maxSize);
Hy = zeros (size (Ez));

% �������� ��������� ���� � ���������� ������ �������
% Ez(q - 1), Hy(q - 1/2)
Ez_prev = zeros (size (Ez));
Hy_prev = zeros (size (Hy));

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    Ez_prev = Ez;
    Hy_prev = Hy;
    
    % ������ ���������� ���� H
    for m = 1: maxSize - 1
        Hy(m) = Hy_prev(m) + (Ez_prev(m + 1) - Ez_prev(m)) * Sc / W0;
    end
    
    % ������ ���������� ���� E
    for m = 2: maxSize
        Ez(m) = Ez_prev(m) + (Hy(m) - Hy(m - 1)) * Sc * W0;
    end

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