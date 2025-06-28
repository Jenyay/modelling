%% ���������� FDTD.
% ������� ������� ���������������� � ���� ������� (TFSF boundary)
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� ������� � ��������
maxTime = 350;

% ������ ������� ������������� � ��������
maxSize = 200;

% ��������� �������, ��������������� ����
probePos = 60;

% ��������� ��������� �����������
sourcePos = 50;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize);

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    Hy(maxSize) = Hy(maxSize - 1);
    
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(n) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0;
    end
    
    % �������� ����������� � �������������� ������ 
    % Total Field / Scattered Field
    % Hy(sourcePos - 1) = Hy(sourcePos - 1) - ...
    %    exp (-(t - 30.0 - sourcePos) ^ 2 / 100.0) / W0;
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) - ...
       exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % ������ ���������� ���� E
    Ez(1) = Ez(2);
    
    for m = 2: maxSize
        % �� ���� ������ Ez(n) ������ �������� ���������� Ez
        % �� ���������� ������ �������
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * W0;
    end

    % �������� ����������� � �������������� ������ 
    % Total Field / Scattered Field
    % Ez(sourcePos) = Ez(sourcePos) +...
    %    exp (-((t + 0.5) - (sourcePos - 0.5) - 30.0) ^ 2 / 100.0);
    
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-((t + 0.5) - (-0.5) - 30.0) ^ 2 / 100.0);
       
    % ����������� ���� � �����
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
    title (sprintf('%d', t))
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