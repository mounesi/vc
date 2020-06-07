function [Plants, Desired_Margins, LB,  UB , x0, frdfreq, Num_Plants, T , notch_length] = read_plants_targets_knobs()

edit read_plants_targets_knobs cost_at_margin control_builder NotchTFs margin_calculator simulate_plots EXE_controller_buildup 


load('TFMAIN4')
Plants{1} = TF.hysv40 ; 
Plants{2} = TF.hysv40No ; 
Plants{3} = TF.hysv40Dbl ; 

Num_Plants = numel(Plants); 

% sampling time
T = 0.002; 

% frequncy
frdfreq = Plants{1, 1}.Frequency/2/pi;

%%
Desired_Margins.GM.Target = 4;  % db
Desired_Margins.GM.Weight = 10;

Desired_Margins.PM.Target = 40;  % degree
Desired_Margins.PM.Weight = 10;   %10;
 
Desired_Margins.BW.Target = 5; % Hz
Desired_Margins.BW.Weight = 1;

Desired_Margins.ETFUB.Frequency = [0.2 4.5 20 250];%  [500 1000 10000 20001]; % Hz
Desired_Margins.ETFUB.Target = [-20 -4 6 2]; % dB
Desired_Margins.ETFUB.Weight = [10 10 10 10];

 for ix = 1:length(frdfreq); 
     indFreq = find(Desired_Margins.ETFUB.Frequency > frdfreq(ix),1);
     Desired_Margins.ETFUB.TargetVec(ix) = Desired_Margins.ETFUB.Target(indFreq);
     Desired_Margins.ETFUB.WeightVec(ix) = Desired_Margins.ETFUB.Weight(indFreq);
 end

 Desired_Margins.OLUB.Frequency = [20 250]; % Hz
 Desired_Margins.OLUB.Target = [50 -10]; % dB 
 Desired_Margins.OLUB.Weight = [10 10]; 
 for ix = 1:length(frdfreq)
     indFreq = find(Desired_Margins.OLUB.Frequency > frdfreq(ix),1);
     Desired_Margins.OLUB.TargetVec(ix) = Desired_Margins.OLUB.Target(indFreq);
     Desired_Margins.OLUB.WeightVec(ix) = Desired_Margins.OLUB.Weight(indFreq);
 end

 %%
% Control Knobs
%kp = 20000; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&&&& kp min

kp = 5;
kp_min = 1e-6; 
kp_max = 1e6;

% ki = 100;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&&&& ki min
ki = 10;
ki_min = 5; 
ki_max = 1000;  

%aNum  = 8;
aNum = 20;
aNum_min = 1;
aNum_max = 1000;

%bDen  = 8;
bDen = 20;
bDen_min = 1;
bDen_max = 1000;

%NDepth_vec = [30 10 1]; 
NDepth_vec = [ 20, 7, 7];%, 5, 5]; 
NDepth_vec_min = [ 1 1 1 ];%1 1];   
NDepth_vec_max = [35 20 20];% 25 25]; 

%NWidth_vec = [10 5 1];
NWidth_vec = [ 10, 3, 3];% , 2, 2];
NWidth_vec_min = [ 1 1 1];% 1 1]; 
NWidth_vec_max = [30 30 30];% 20 20]; 

%NFreq_vec = [84 292 712]/(2*pi);
NFreq_vec = [4.35, 27, 27.6];%, 76.7, 165];
NFreq_vec_min = [2 2 2];% 2 2]; 
NFreq_vec_max = [250 250 250];% 250 250];

notch_length = length(NFreq_vec); 

x0 = [kp ki aNum bDen NDepth_vec NWidth_vec NFreq_vec];
LB = [kp_min ki_min aNum_min bDen_min NDepth_vec_min NWidth_vec_min NFreq_vec_min];
UB = [kp_max ki_max aNum_max bDen_max NDepth_vec_max NWidth_vec_max NFreq_vec_max];

%assignin ('base', 'Control_Knobs',Control_Knobs)