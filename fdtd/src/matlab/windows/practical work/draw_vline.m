%% Функция для рисовани вертикальной линии на графике
function draw_vline (x, ymin, ymax)
    line ([x, x], [ymin, ymax], 'Color',[0.0, 0.0, 0.0]);
end