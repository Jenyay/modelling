%% ���������� FDTD. ������ 1.7.1
% �������� ����������� � ���� �������� ������.
% ������������ ����� TFSF.
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� ������� � ��������
maxTime = 300;

% ������ ������� ������������� � ��������
maxSize = 200;

% ��������� �������, ��������������� ����
probePos = 50;

% ��������� ��������� �����������
sourcePos = 50;

Sc = 1.0;
Np = 30;
Md = 2.5;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(n) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0;
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) - ...
        (1 - 2 * pi ^ 2 * (Sc * t / Np - Md) ^ 2) *...
        exp (-pi ^ 2 * (Sc * t / Np - Md) ^ 2) / W0;
    
    % ������ ���������� ���� E
    Ez(1) = Ez(2);
    Ez(end) = Ez(end - 1);
    
    for m = 2: maxSize - 1
        % �� ���� ������ Ez(n) ������ �������� ���������� EzS
        % �� ���������� ������ �������
        % ������ W0 / eps ������������ cezh
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * W0;
    end

    % �������� �����������
    Ez(sourcePos) = Ez(sourcePos) +...
        (1 - 2 * pi ^ 2 * ((Sc * (t + 0.5) - (-0.5)) / Np - Md) ^ 2) *...
        exp (-pi ^ 2 * ((Sc * (t + 0.5) - (-0.5)) / Np - Md) ^ 2);
    
    % ����������� ���� � �����
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
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