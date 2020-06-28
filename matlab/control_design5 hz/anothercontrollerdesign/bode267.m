function bode267(sys_z, a )

 
    opts = bodeoptions; 
    %opts.MagUnits = 'abs' ; 
    opts.FreqUnits = 'Hz';
    %opts.FreqScale = 'log'; 
    opts.Xlim = [0.1 500];
    %opts.MagScale = 'linear';
    opts.Xlabel.FontSize = 14 ; 
    opts.Ylabel.FontSize = 14 ;
    opts.Title.String = a ; 
    opts.Title.FontSize = 14;
    opts.Title.Color = [1 0 0];
    opts.TickLabel.FontSize = 12 ; 
    opts.Grid = 'on' ; 
    opts.GridColor = 'r' ; 

bode (sys_z, opts) ; 


h = findobj(gcf,'type','line');
set(h,'linewidth',3);
    

end 
