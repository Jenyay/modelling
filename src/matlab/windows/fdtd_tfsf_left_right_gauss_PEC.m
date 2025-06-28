%% ���������� FDTD.
% ������� ������� ���������������� � ���� ������� (TFSF boundary)
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� ������� � ��������
maxTime = 450;

% ������ ������� ������������� � ��������
maxSize = 350;

% ��������� �������, ��������������� ����
probePos = 60;

% ��������� ��������� �����������
%sourcePos = 50;

% ����� ������� TFSF
tfsf_left = 50;

% ������ ������� TFSF
tfsf_right = 250;

% ��������� �������������� �����
PEC_x = 150;

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
    Hy(tfsf_left - 1) = Hy(tfsf_left - 1) - ...
        exp (-(t - 30.0 - tfsf_left) ^ 2 / 100.0) / W0;

    Hy(tfsf_right - 1) = Hy(tfsf_right - 1) + ...
        exp (-(t - 30.0 - tfsf_right) ^ 2 / 100.0) / W0;
    
%     Hy(tfsf_left - 1) = Hy(tfsf_left - 1) - ...
%         exp (-(t - 30.0 - (tfsf_left - tfsf_left)) ^ 2 / 100.0) / W0;
% 
%     Hy(tfsf_right - 1) = Hy(tfsf_right - 1) + ...
%         exp (-(t - 30.0 - (tfsf_right - tfsf_left)) ^ 2 / 100.0) / W0;
    
    % ������ ���������� ���� E
    Ez(1) = Ez(2);
    
    for m = 2: maxSize
        % �� ���� ������ Ez(n) ������ �������� ���������� EzS
        % �� ���������� ������ �������
        Ez(m) = Ez(m) + (Hy(m) - Hy(m - 1)) * W0;
    end

    % �������� ����������� � �������������� ������ 
    % Total Field / Scattered Field
    Ez(tfsf_left) = Ez(tfsf_left) + ...
        exp (-(t + 0.5 - (tfsf_left - 0.5) - 30.0) ^ 2 / 100.0);
    
    Ez(tfsf_right) = Ez(tfsf_right) - ...
        exp (-(t + 0.5 - (tfsf_right - 0.5) - 30.0) ^ 2 / 100.0);
    
%     Ez(tfsf_left) = Ez(tfsf_left) + ...
%         exp (-(t + 0.5 - (tfsf_left - tfsf_left - 0.5) - 30.0) ^ 2 / 100.0);
%     
%     Ez(tfsf_right) = Ez(tfsf_right) - ...
%         exp (-(t + 0.5 - (tfsf_right - tfsf_left - 0.5) - 30.0) ^ 2 / 100.0);
    
    % ������������� ���� � ������� �������������
    Ez(PEC_x) = 0;

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
    plot (tfsf_left, 0, '*r');
    plot (tfsf_right, 0, '*r');
    line ([PEC_x, PEC_x], [-1.1, 1.1], ...
        'Color',[0.0, 0.0, 0.0]);
    hold off
    pause (0.03)
end

figure
plot (probeTimeEz)
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on