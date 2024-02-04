%% Сравнение коэффициента отражения для непрерывного случая и с использованием метода FDTD

function reflection_error
    Nl = 10: 80;
    eps1 = 1;
    mu1 = 1;
    
    eps2 = 4;
    mu2 = 1;
    
    figure
    hold on
    legends = {};
    for Sc = 1: -0.25: 0.25
        legend_str = sprintf('Sc = %.2f', Sc);
        legends{end + 1} = legend_str;
        
        phase1 = get_phase (eps1, mu1, Sc, Nl);
        phase2 = get_phase (eps2, mu2, Sc, Nl);
        
        ref_fdtd = (sqrt(eps1) .* cos (phase2) - sqrt(eps2) .* cos (phase1)) ./ ...
            (sqrt(eps1) .* cos (phase2) + sqrt(eps2) .* cos (phase1));

        plot (Nl, ref_fdtd);
    end
    
    ref_anal = ones (size(Nl)) .* (sqrt(eps1) - sqrt(eps2)) / (sqrt(eps1) + sqrt(eps2));
    plot (Nl, ref_anal, '--k');
    legends{end + 1} = 'Аналитика';
    
    grid on
    legend (legends, 'Location','southeast');
    hold off
    xlabel ('$$N_\lambda$$', 'Interpreter','latex', 'FontSize', 14)
    ylabel ('|Г|', 'FontSize', 14)
end


function phi = get_phase (eps, mu, Sc, Nl)
    phi = asin (sqrt (eps .* mu) .* sin (pi .* Sc ./ Nl) ./ Sc);
end