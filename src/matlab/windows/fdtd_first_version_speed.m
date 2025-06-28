%% ���������� FDTD.
% ������ �������� ��������������� �����
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� ������� � ��������
maxTime = 250;

% ������ ������� ������������� � ��������
maxSize = 200;

% ��������� �������, ��������������� ����
probePos_1 = 50;
probePos_2 = 150;

Ez = zeros (1, maxSize);
Hy = zeros (size (Ez));

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz_1 = zeros (1, maxTime);
probeTimeEz_2 = zeros (1, maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(n) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0;
    end
    
    % ������ ���������� ���� E
    for m = 2: maxSize
        % �� ���� ������ Ez(n) ������ �������� ���������� Ez
        % �� ���������� ������ �������
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * W0;
    end

    % �������� �����������
    Ez(1) = exp (-(t - 30.0) ^ 2 / 100.0);
    
    % ����������� ���� � �����
    probeTimeEz_1(t) = Ez(probePos_1);
    probeTimeEz_2(t) = Ez(probePos_2);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
    grid on
    
    hold on
    plot (probePos_1, 0, 'xk');
    plot (probePos_2, 0, 'xk');
    hold off
    
    pause (0.03)
end

figure
hold on
plot (probeTimeEz_1, 'b')
plot (probeTimeEz_2, 'r')
hold off
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on