function simulate_plots(C_z); 


    opts = bodeoptions; 
    opts.FreqUnits = 'Hz';

    TF = evalin('base','TF');
    Plants{1} = TF.hysv40;
    Plants{2} = TF.hysv40Dbl;
    Plants{3} = TF.hysv40No;

    
margins = margin_cal(C_z,Plants); 

% Open loop; 
frdfreq = TF.hysv40.Frequency/2/pi;
figure; 
   plot (frdfreq, Desired_Margins.OLUB.TargetVec);
   hold on;
for i = 1:Num_Plants ; 
   bode(margins.OL_DD{i},opts);
end
title('OL')
hold off

% ETF; 
figure;
plot(frdfreq, Desired_Margins.ETFUB.TargetVec);
hold on ; 
for i = 1:Num_Plants ; 
    bode(margins.ETF_DD{i},opts);
end
title('ETF')

% margins 
figure;  
subplot(3,1,1)
Nm = numel(margins.GM)-1;
plot(sort(margins.GM),[0:1/Nm:1]);
xlabel('GM [dB]')

subplot(3,1,2)
Nm = numel(margins.PM)-1;
plot(sort(margins.PM),[0:1/Nm:1]);
xlabel('PM [deg]')

subplot(3,1,3)
Nm = numel(margins.BW)-1;
plot(sort(margins.BW),[0:1/Nm:1]);
xlabel('BW [Hz]')







