%% ���������� FDTD. ������ 1.5
% ����� � ��������.
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� ������� � ��������
maxTime = 450;

% ������ ������� ������������� � ��������
maxSize = 200;

% ��������� ���������
sourcePos = 50;

% ��������� ��������, �������������� ����, � ��������
probePos = [110, 130, 150, 170];

% ������ ���� � ��������
layer_x = 100;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

% ������ � �����. loss = sigma * dt / (2 * eps * eps0)
loss = zeros (1, maxSize);
loss(layer_x: end) = 0.01;

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

ceze = (1 - loss) ./ (1 + loss);
cezh = W0 ./ (eps .* (1 + loss));

% ����, ������������������ � �������� � ����������� �� �������
% ������ ������ - ����� �������,
% ������ ������ - ��������� ������.
probeTimeEz = zeros(size(probePos, 2), maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(n) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0;
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1)...
        - exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % ������ ���������� ���� E
    % �.�. ���� ������ ���������� ��������� ������� � ��� �� ��������,
    % ������ ��������� ������� ������.
    Ez(1) = Ez(2);
    
    for m = 2: maxSize - 1
        % �� ���� ������ Ez(n) ������ �������� ���������� EzS
        % �� ���������� ������ �������
        % ������ W0 / eps ������������ cezh
        Ez(m) = ceze(m) * Ez(m) + ...
            cezh(m) * (Hy(m) - Hy(m - 1));
    end

    % �������� �����������
    Ez(sourcePos) = Ez(sourcePos) +...
        exp (-(t + 0.5 - (-0.5) - 30.0) ^ 2 / 100.0);
    
    % ����������� ���� � ��������
    for p = 1:size(probePos, 2)
        probeTimeEz(p, t) = Ez(probePos(p));
    end;
    
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
hold on
for p = 1:size(probePos, 2)
    plot (probeTimeEz(p,:))
end
hold off
xlabel ('t, ������')
ylabel ('Ez, �/�')
grid on