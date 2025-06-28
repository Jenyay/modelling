%% ���������� FDTD.
% ����������� ��������� ���� E � H
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

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
probeTimeHy = zeros (1, maxTime);

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
    probeTimeEz(t) = Ez(probePos);
    probeTimeHy(t) = Hy(probePos);
    
    subplot (2, 1, 1)
    plot (Ez, 'b');
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
    grid on
    hold on
    plot (probePos, 0, 'xk');
    hold off
    
    subplot (2, 1, 2)
    plot (Hy, 'r');
    xlim ([1, maxSize]);
    ylim ([-1.1 / 377, 1.1 / 377]);
    xlabel ('x, ������')
    ylabel ('Hy, �/�')
    grid on
    hold on
    plot (probePos, 0, 'xk');
    hold off
    
    pause (0.03)
end

figure
subplot (2, 1, 1)
plot (probeTimeEz, 'b')
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on

subplot (2, 1, 2)
plot (probeTimeHy, 'r')
xlabel ('t, ������')
ylabel ('Hy, �/�')
grid on