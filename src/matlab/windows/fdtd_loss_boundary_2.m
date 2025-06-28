%% ���������� FDTD. ������ 1.6.1
% ������� ������� ������ - ����������.
% �� ������ ������� ������� ���������� ���������� � ��������.
% ��������� ���������� ������������� ��� ������� ��������� �� �������
% ������������ ����.
clear

% �������� ������������� ���������� ������������
W0 = 120 * pi;

% ����� ������� � ��������
maxTime = 750;

% ������ ������� ������������� � ��������
maxSize = 200;

% ��������� ���������
sourcePos = 50;

% ��������� �������, ��������������� ����
probePos = 60;

% ������ ���������������� ����
layer_x = 100;

% ��� ���������� ����������� ����������
layer_loss_x = 160;

% ������ � �����. loss = sigma * dt / (2 * eps * eps0)
loss = zeros(1, maxSize);
loss(layer_loss_x: end) = 0.01;

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (size (Ez));
eps(layer_x: end) = 9.0;

% ������������ ��� ������� ���� E
ceze = (1 - loss) ./ (1 + loss);
cezh = W0 ./ (eps .* (1 + loss));

% ���������� ������������� �� ������� ������������ ����
ceze(layer_loss_x) = (ceze(layer_loss_x - 1) +...
    ceze(layer_loss_x + 1)) / 2;
cezh(layer_loss_x) = (cezh(layer_loss_x - 1) +...
    cezh(layer_loss_x + 1)) / 2;

% ������������ ��� ������� ���� H
chyh = (1 - loss) ./ (1 + loss);
chye = 1 ./ (W0 * (1 + loss));

% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (1, maxTime);

figure

for t = 1: maxTime
    % ������ ���������� ���� H
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(n) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = chyh(m) * Hy(m) + ...
            chye(m) * (Ez(m + 1) - Ez(m));
    end
    
    Hy(sourcePos - 1) = Hy(sourcePos - 1) - ...
        exp (-(t - 30.0) ^ 2 / 100.0) / W0;
    
    % ������ ���������� ���� E
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
    
    % ����������� ���� � �����
    probeTimeEz(t) = Ez(probePos);
    
    plot (Ez);
    xlim ([1, maxSize]);
    ylim ([-1.1, 1.1]);
    xlabel ('x, ������')
    ylabel ('Ez, �/�')
    line ([layer_x, layer_x], [-1.1, 1.1], ...
        'Color',[0.0, 0.0, 0.0]);
    line ([layer_loss_x, layer_loss_x], [-1.1, 1.1], ...
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