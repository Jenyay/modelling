%% ������ ������� �������� ������
clear

% ������ �������
size = 1024;

% ��� �� �������
dt = 0.4e-10;

% ��� �� �������
df = 1.0 / (size * dt);

fp = 1e9;
Md = 1.7;
dr = Md / fp;

% ������� ������
time = (0:size - 1) * dt;
impulse = (1 - 2 * (pi * fp * (time - dr)) .^ 2) .*...
    exp (-(pi * fp * (time - dr)) .^ 2);

% ������ �������
spectrum = fft(impulse);
spectrum = fftshift (spectrum);

% ������ �������
freq = (-size / 2:size / 2 - 1) * df;

% ����������� ��������
subplot (1, 2, 1)
plot (time, impulse)
xlim ([0, 0.4e-8]);
grid on
xlabel ('�����, �')
ylabel ('Ez')

% ����������� �������
subplot (1, 2, 2)
plot (freq, abs (spectrum))
grid on
xlabel ('�������, ��')
ylabel ('|P|')
xlim ([0, 5e9]);
set(gca,'XTick',[-5e9: 1e9: 5e9])