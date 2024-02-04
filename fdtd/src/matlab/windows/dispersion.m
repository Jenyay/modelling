%% Расчет отношений фазовых скоростей для непрерывного и дискретного случаев

function dispersion
    Nl = 3:20;
    eps = 1;
    mu = 1;
    
    figure
    hold on
    legends = {};
    for Sc = 1: -0.25: 0.25
        legend_str = sprintf('Sc = %.2f', Sc);
        legends{end + 1} = legend_str;
        ratio = abs (getDispersionRatio (Sc, Nl, eps, mu));

        plot (Nl, ratio);
    end
    
    grid on
    legend (legends, 'Location','southeast');
    ylim ([0.6, 1.05])
    xlabel ('$$N_\lambda$$', 'Interpreter','latex', 'FontSize', 14)
    ylabel ('$${\widetilde{c}} \over c$$',...
        'Interpreter','latex',...
        'Rotation', 0,...
        'FontSize', 14)
    hold off
end


function ratio = getDispersionRatio (Sc, Nl, eps, mu)
    numerator = pi .* sqrt (eps .* mu);
    denominator = Nl .* asin (sqrt (eps .* mu) .* sin (pi .* Sc ./ Nl) ./ Sc);
    ratio = numerator ./ denominator;
end