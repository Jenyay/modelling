%% Расчет коэффициента отражения от слоистой среды

src = probeTimeEz;

inc = probeTimeEz;
inc(81:end) = 0;

ref = probeTimeEz;
ref (1: 81) = 0;

inc_sp = fft(inc);
ref_sp = fft(ref);
r = ref_sp ./ inc_sp;
r_abs = abs (r);

figure
subplot (4, 2, 1);
plot (src);
grid on

subplot (4, 2, 3);
plot (inc);
grid on

subplot (4, 2, 4);
plot (abs (inc_sp));
xlim([0, 120]);
grid on

subplot (4, 2, 5);
plot (ref);
grid on

subplot (4, 2, 6);
plot (abs (ref_sp));
xlim([0, 120]);
grid on

subplot (4, 2, 8);
plot (r_abs);
xlim([0, 120]);
ylim ([0, 1]);
grid on