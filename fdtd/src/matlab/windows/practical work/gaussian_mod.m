function result = gaussian_mod(x, t, Sc, N0, Nd, Nw)
%gaussian_mod Функция плоской волны для модулированного гауссова сигнала.
    result = sin(2 * pi ./ N0 .* (t ./ Sc + x)) .*...
        exp (-((t + x ./ Sc - Nd) ./ Nw) .^ 2);
end

