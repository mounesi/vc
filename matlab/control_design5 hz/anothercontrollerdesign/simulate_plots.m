function simulate_plots(C_z, x); 


Desired_Margins = evalin('base','Desired_Margins'); 
T = evalin('base','T');
Num_Plants = evalin('base','Num_Plants');
Plants = evalin('base','Plants');
frdfreq = evalin('base', 'frdfreq');

%% Margin Calculator; 
margins = margin_calculator(C_z, Plants); 

% Open loop; 
figure; 
   plot (frdfreq, Desired_Margins.OLUB.TargetVec);
   hold on;
for i = 1:Num_Plants ; 
   bode267(margins.OL_DD{i},'Open-Loop Transfer Function');
end
hold off


% ETF; 
figure;
plot(frdfreq, Desired_Margins.ETFUB.TargetVec);
hold on ; 
for i = 1:Num_Plants ; 
    bode267(margins.ETF_DD{i},'Sensitivity Transfer Function');
end

% Disturbance TF (Plant*Controller); 
figure;
hold on ; 
for i = 1:Num_Plants ; 
    bode267(margins.ETF_DD{i}*Plants{i},'Disturbance Transfer Function');
    bode267(Plants{i},'Disturbance Transfer Function');
end

%%
figure;  

subplot(3,1,1)
Nm = numel(margins.GM)-1;
plot(sort(margins.GM),[0:1/Nm:1],'-*');
xlabel('GM [dB]')

subplot(3,1,2)
Nm = numel(margins.PM)-1;
plot(sort(margins.PM),[0:1/Nm:1],'-*');
xlabel('PM [deg]')

subplot(3,1,3)
Nm = numel(margins.BW)-1;
plot(sort(margins.BW),[0:1/Nm:1],'-*');
xlabel('BW [Hz]')

%%
figure; bode(C_z)



