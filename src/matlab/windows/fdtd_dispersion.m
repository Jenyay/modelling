%% ���������� FDTD. ������ 1.3
% ������� ������� ���������������� � ���� ������� (TFSF boundary)
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� ������� � ��������
maxTime = 1024;

% ������ ������� ������������� � ��������
maxSize = 2000;

% ��������� �������, ��������������� ����
probePos = 1500;

% ��������� ��������� �����������
sourcePos = 1200;

Sc = 0.5;

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
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) * Sc / W0;
    end
    
    % ������ ���������� ���� E
    Ez(1) = Ez(2);
    for m = 2: maxSize
        % �� ���� ������ Ez(n) ������ �������� ���������� EzS
        % �� ���������� ������ �������
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * Sc * W0;
    end

    % �������� �����������
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 50.0) ^ 2 / 50.0) * Sc;
    
    % ����������� ���� � �����
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1000, 1600]);
    ylim ([-0.6, 0.6]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
    grid on
    hold on
    plot (probePos, 0, 'xk');
    plot (sourcePos, 0, '*r');
    hold off
    pause (0.01)
end

spectrum = fft(probeTimeEz);
spectrum_abs = abs(spectrum);
spectrum_phase = unwrap(angle(spectrum));

figure
% ������ � �������
subplot(3, 1, 1)
plot (probeTimeEz)
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on

% ����������� ������ ������� � �������
subplot(3, 1, 2)
plot (spectrum_abs)
xlabel ('f')
ylabel ('|Ez|, �/(�*��)')
xlim([0, 300])
grid on

% ������� ������ ������� � �������
subplot(3, 1, 3)
plot (spectrum_phase)
xlabel ('f')
ylabel ('Phase(Ez), ���.')
xlim([0, 300])
grid on
