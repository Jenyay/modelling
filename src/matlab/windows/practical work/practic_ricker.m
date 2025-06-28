%% ������ ������������ ��������� �� �������������� �����
% ��� ��������� �������� � ����������� �������
% ������ 1.1 (02.05.2016)
clear
clc

% ********************
% �������� ������
% ������ �����
dx = 1 * 1e-3;

% ������ ������� ������������� � ������
maxSize_m = 0.4;

% ����� ������������� � ��������
maxTime_sec = 12e-9;

layers_begin = [0.2, 0.3];
layers_eps = [9.0, 3.0];
layers_mu = [1.0, 1.0];
layers_sigma = [0.0, 0.0];

% ��������� �������, ��������������� ���� Ez, � ������
probePos_m = 0.06;

% ��������� ����� ����������� � ������
port_x_m = 0.04;

fmin = 2e9;
fmax = 5e9;

% ����� �������
Sc = 1.0;

% �������� ���������� ��������
speed = 5;

% ��������� ��������� �������, � ��������
inc_time_s = 1.0e-9;


% ********************

% �������� �������� ������ ��� ������� ���������� ����
assert (all (layers_eps >= 1))
assert (all (layers_mu >= 1))
assert (all (layers_sigma >= 0))
assert (all (size(layers_begin) == size(layers_eps)));
assert (all (size(layers_begin) == size(layers_mu)));

% �������� ����� � �������
c = 299792458;

% �������� ������������� ���������� ������������
eps0 = 8.854187817e-12;
W0 = 120 * pi;

% ��������� ��� � ��������
dt = Sc * dx / c;

% ������ ���������� ��������
fp = (fmax + fmin) / 2;
Md = 2;
dr = Md / fp;
Np = (dr * Sc) / (Md * dt);

% ������ "����������" ����������
% ����� ������� � ��������
maxTime = ceil (maxTime_sec / dt);

% ������ ������� ������������� � ��������
maxSize = ceil (maxSize_m / dx);

% ��������� ��������, ��������������� ����
probePos = ceil (probePos_m / dx);

% ���������� ��������
probeCount = size (probePos, 2);

% ��������� ����� �����������
port_x = ceil (port_x_m / dx);

% ��������� ���������� ����
inc_time = ceil (inc_time_s / dt);

fprintf ('dx = %.3f ��;\n', dx * 1e3);
fprintf ('dt = %6.5e �;\n', dt);
fprintf ('����� �������: %.3f;\n', Sc);
fprintf ('������� �������������: %.3f � (%d �����);\n', maxSize_m, maxSize);
fprintf ('����� �������������: %e � (%d ��������� ��������);\n', maxTime_sec, maxTime);
fprintf ('��������� ����� �����������: %.3f � (%d �����);\n', port_x_m, port_x);
fprintf ('��������� ��������:\n');
for probe=1:probeCount
    fprintf ('    %d. %.3f � (%d �����);\n',...
        probe, probePos_m(probe), probePos(probe));
end

Ez = zeros (1, maxSize);
Hy = zeros (1, maxSize - 1);

eps = ones (1, size (Ez));
mu = ones (1, size (Ez));
sigma = zeros (1, size (Ez));

% �������� �����
layers_count = size(layers_begin, 2);
for n = 1:layers_count
    begin = ceil(layers_begin(n) / dx) + 1;
    eps(begin: end) = layers_eps(n);
    mu(begin: end) = layers_mu(n);
    sigma(begin: end) = layers_sigma(n);
end

% ������������ ��� ����� ������������
loss = sigma * dt ./ (2 * eps * eps0);
ceze = (1 - loss) ./ (1 + loss);
cezh = (W0 ./ eps) ./ (1 + loss);

% ������������ ��� ������� ABC ������ ������� �� ����� �������

% Sc' ��� ����� �������
Sc1Left = Sc / sqrt (mu(1) * eps(1));

k1Left = -1 / (1 / Sc1Left + 2 + Sc1Left);
k2Left = 1 / Sc1Left - 2 + Sc1Left;
k3Left = 2 * (Sc1Left - 1 / Sc1Left);
k4Left = 4 * (1 / Sc1Left + Sc1Left);

% Sc' ��� ������ �������
Sc1Right = Sc / sqrt (mu(end) * eps(end));

k1Right = -1 / (1 / Sc1Right + 2 + Sc1Right);
k2Right = 1 / Sc1Right - 2 + Sc1Right;
k3Right = 2 * (Sc1Right - 1 / Sc1Right);
k4Right = 4 * (1 / Sc1Right + Sc1Right);

% Ez(1), Ez(2), Ez(3) � ���������� ������ ������� (q)
oldEzLeft1 = zeros(3);
oldEzRight1 = zeros(3);

% Ez(1), Ez(2), Ez(3) � ����-���������� ������ ������� (q-1)
oldEzLeft2 = zeros(3);
oldEzRight2 = zeros(3);


% ����, ������������������ � ������� � ����������� �� �������
probeTimeEz = zeros (probeCount, maxTime);
probe_y = zeros (size (probePos));

x_m = (1:maxSize) * dx;

figure     

for t = 0: maxTime
    % ������ ���������� ���� H
    for m = 1: maxSize - 1
        % �� ���� ������ Hy(n) ������ �������� ���������� Hy
        % �� ���������� ������ �������
        Hy(m) = Hy(m) + (Ez(m + 1) - Ez(m)) / W0 / mu(m);
    end
    
    Hy(port_x - 1) = Hy(port_x - 1) - ricker_1d (0, t, Sc, Np, Md) / W0;
    
    % ������ ���������� ���� E
    for m = 2: maxSize - 1
        % �� ���� ������ Ez(n) ������ �������� ���������� EzS
        % �� ���������� ������ �������
        Ez(m) = ceze(m) * Ez(m) + cezh(m) * (Hy(m) - Hy(m - 1));
    end

    % �������� �����������
    Ez(port_x) = Ez(port_x) + ricker_1d (0.5, t + 0.5, Sc, Np, Md);
    
    % ��������� ������� ABC ������ ������� (�����)
    Ez(1) = k1Left * (k2Left * (Ez(3) + oldEzLeft2(1)) +...
        k3Left * (oldEzLeft1(1) + oldEzLeft1(3) - Ez(2) - oldEzLeft2(2)) - ...
        k4Left * oldEzLeft1(2)) - oldEzLeft2(3);
    
    oldEzLeft2 = oldEzLeft1;
    oldEzLeft1 = Ez(1:3);
    
    % ��������� ������� ABC ������ ������� (������)
    Ez(end) = k1Right * (k2Right * (Ez(end - 2) + oldEzRight2(end)) +...
        k3Right * (oldEzRight1(end) + oldEzRight1(end - 2) - Ez(end - 1) - oldEzRight2(end - 1)) - ...
        k4Right * oldEzRight1(end - 1)) - oldEzRight2(end - 2);
    
    oldEzRight2 = oldEzRight1;
    oldEzRight1 = Ez(end-2: end);
    
    % ����������� ���� � �����
    for probe=1:probeCount
        probeTimeEz(probe, t + 1) = Ez(probePos(probe));
    end
    
    if mod (t, speed) == 0 || t == maxTime
        plot (x_m, Ez, '-b',...
              probePos_m, probe_y, 'kx',...
              port_x_m, 0, '*r');

        xlim ([0, maxSize_m]);
        ylim ([-1.1, 1.1]);
        xlabel ('x, ��')
        ylabel ('Ez, �/�')
        
        for n = 1:layers_count
            draw_vline (layers_begin(n), -1.1, 1.1)
        end
        
        percent = t / maxTime * 100;
        title_str = sprintf ('%.3f �� (%.0f %%)', t * dt * 1e9, percent);
        title (title_str);
        grid on
        pause (0.01)
    end
end

% ����� �������� �� ���������
figure
hold on

time = (0:maxTime) * dt;
for probe=1:probeCount
    plot (time, probeTimeEz(probe, :))
end

% ���������� ������ ��������
probeLegend = {zeros(probeCount)};
for probe=1:probeCount
    probeLegend(probe) = cellstr (sprintf ('x = %.3f mm', ...
        probePos_m(probe) * dx * 1e3));
end

% ���������� ������� � ��������� � ���������
xlabel ('t, �')
ylabel ('Ez, �/�')
legend (probeLegend);
grid on
hold off

% ��������� �����������
df = 1.0 / maxTime_sec;
freq = (0: maxTime) * df;

% ������ � ������ �������
full_signal = probeTimeEz(1, :);

% ��������� ��������� �������
inc_signal = full_signal;
inc_signal(inc_time: end) = 0;

% ������ ������� ��������� �������
inc_spectrum = fft (inc_signal);
inc_spectrum_abs = abs (inc_spectrum);

% ��������� ����������� �������
ref_signal = full_signal;
ref_signal(1: inc_time - 1) = 0;

% ������ ������� ����������� �������
ref_spectrum = fft (ref_signal);
ref_spectrum_abs = abs (ref_spectrum);

% ������ ������ ������������ ���������
r = abs (ref_spectrum ./ inc_spectrum);

figure;
% ����� ��������� �������
subplot (3, 2, 1);
plot (time * 1e9, inc_signal);
xlabel ('�����, ��')
ylabel ('Ez')
title ('�������� ������')
draw_vline (inc_time_s * 1e9, -1.1, 1.1)
ylim ([-1.1, 1.1]);
grid on

% ����� ������� ��������� �������
subplot (3, 2, 2);
plot (freq * 1e-9, inc_spectrum_abs);
xlim ([fmin * 1e-9, fmax * 1e-9]);
xlabel ('�������, ���')
ylabel ('|S|')
title ('������ ��������� �������')
grid on

% ����� ����������� �������
subplot (3, 2, 3);
plot (time * 1e9, ref_signal);
xlabel ('�����, ��')
ylabel ('Ez')
title ('���������� ������')
draw_vline (inc_time_s * 1e9, -1.1, 1.1)
ylim ([-1.1, 1.1]);
grid on

% ����� ������� ����������� �������
subplot (3, 2, 4);
plot (freq * 1e-9, ref_spectrum_abs);
xlim ([fmin * 1e-9, fmax * 1e-9]);
xlabel ('�������, ���')
ylabel ('|S|')
title ('������ ����������� �������')
grid on

% ����� ���������� �������
subplot (3, 2, 5);
plot (time * 1e9, full_signal);
xlabel ('�����, ��')
ylabel ('Ez')
title ('��������� ������')
draw_vline (inc_time_s * 1e9, -1.1, 1.1)
ylim ([-1.1, 1.1]);
grid on

% ����� ������������ ���������
subplot (3, 2, 6);
plot (freq * 1e-9, r);
xlim ([fmin * 1e-9, fmax * 1e-9]);
ylim ([0, 1.0]);
xlabel ('�������, ���')
ylabel ('|S|')
title ('����������� ���������')
grid on