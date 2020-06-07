%%

%%
% step 1 Read the plants manually
load('TFMAIN4.mat')
% step 2 define parameters
%%
v.num_plants = 3 ; 
v.tim_sampl = 0.002 ;
v.freq_vec = TF.v20.Frequency/2/pi;
v.GM.Target = 4 ; % db
v.GM.Weight = 1; 
v.PM.Target = 30 ; %degree
v.PM.Weight = 1 ; 
v.BW.Target = 5; % Hz
v.BW.Weight = 1; 

v.ETFUB.Freq = [6 250]; 
v.ETFUB.Target = [8 2]; % db
v.ETFUB.Weight = [10 10]; 
%%
for ii = 1: length(v.freq_vec); 
    indOFfreq = find(v.ETFUB.Freq>v.freq_vec(ii),1); 
    v.ETFUB.TargetVec(ii) = v.ETFUB.Target(indOFfreq); 
    v.ETFUB.WeightVec(ii) = v.ETFUB.Weight(indOFfreq); 
end

v.OLUB.Freq = [5 250]; % Hz
v.OLUB.Target = [100 -8]; % dB
v.OLUB.Weight = [10 10]; 

for jj = 1: length(v.freq_vec); 
    indOFfreq2 = find(v.OLUB.Freq>v.freq_vec(jj),1); 
    v.OLUB.TargetVec(jj) = v.OLUB.Target(indOFfreq2);
    v.OLUB.WeightVec(jj) = v.OLUB.Weight(indOFfreq2); 
end
%%
 % step 3 controller prameters
c.kp = 10620 ; 
c.kp_min = 1; 
c.kp_max = 1e6 ; 

c.ki = 108; 
c.ki_min = 1 ; 
c.ki_max = 1e6; 

c.bDen = 8 ; 
c.bDen_min = 1 ; 
c.bDen_max = 100; 

c.NDepth_vec = [ 20, 20, 7, 7, 1.5 , 1]; 
c.NDepth_vec_min = [ 1 1 1 1 1 1];   
c.NDepth_vec_max = [ 35 35 35 35 35 35]; 

c.NWidth_vec = [ 10, 10, 3, 3, 1.5 1.1];
c.NWidth_vec_min = [ 1 1 1 1 1 1]; 
c.NWidth_vec_max = [20 20 20 20 20 20];

c.NFreq_vec = [4.35, 4.45 27, 27.6, 76.7, 165];
c.NFreq_vec_min = [5 5 5 5 5 5]; 
c.NFreq_vec_max = [500 500 500 500 500 500];

c.notch_length = length(c.NFreq_vec); 

c.Control_Knobs.x0 = [c.kp c.ki c.bDen c.NDepth_vec c.NWidth_vec c.NFreq_vec];
c.Control_Knobs.LB = [c.kp_min c.ki_min c.bDen_min c.NDepth_vec_min c.NWidth_vec_min c.NFreq_vec_min];
c.Control_Knobs.UB = [c.kp_max c.ki_max c.bDen_max c.NDepth_vec_max c.NWidth_vec_max c.NFreq_vec_max];

clear ii jj indOFfreq indOFfreq2
%%

c_z = contr_build(c.Control_Knobs.x0, v.tim_sampl);

simulate_plots(c_z);

%% Optimization

ka = 0; 
options = optimset('MaxFunEvals',200,'Display','iter');
[x_opt f_opt] = fminsearch_con('cost_at_margin',x0,LB,UB,1e20,options);

%% Final Control Values

C_z = control_builder(x_opt)
[CntNum_t,CntDen_t] = tfdata(C_z) 
CntNum = CntNum_t{1,1} ; 
CntDen = CntDen_t{1,1} ; 
