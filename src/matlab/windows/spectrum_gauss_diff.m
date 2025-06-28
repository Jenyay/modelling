%% Расчет спектра дифференцированного гауссова импульса

% Размер массива
size = 512;

% шаг по времени
dt = 0.2e-10;

A_max = 100;
F_max = 3e9;

% Шаг по частоте
df = 1.0 / (size * dt);

w_g = sqrt(log(5.5 * A_max)) / (pi * F_max);
d_g = w_g * sqrt (log (2.5 * A_max * sqrt (log (2.5 * A_max))));

% Дифференцированный гауссов импульс
time = (0:size - 1) * dt;
gauss = -2 * ((time - d_g) / w_g) .* exp (-((time - d_g) / w_g) .^ 2);

% Расчет спектра
spectrum = fft(gauss);
spectrum = fftshift (spectrum);

% Расчет частоты
freq = (-size / 2:size / 2 - 1) * df;

% Отображение импульса
subplot (1, 2, 1)
plot (time, gauss)
xlim ([0, 0.4e-8]);
grid on
xlabel ('Время, с')
ylabel ('Ez')

% Отображение спектра
subplot (1, 2, 2)
plot (freq, abs (spectrum))
grid on
xlabel ('Частота, Гц')
ylabel ('|P|')
xlim ([0, 5e9]);
set(gca,'XTick',[-5e9: 1e9: 5e9])
