function Total_Cost = cost_at_margin( x)

%% Evalin 
T = evalin('base','T');
Num_Plants = evalin('base','Num_Plants');
Plants = evalin('base','Plants');
Desired_Margins = evalin('base', 'Desired_Margins');
C_z = control_builder(x,T);


%% Margin Calculator; 
margins = margin_calculator(C_z,Plants);

%% squred Formula; 

for i = 1 : Num_Plants; 
    
Cost(i) = 0;

if Desired_Margins.GM.Weight > 0
    if margins.GM(i) < Desired_Margins.GM.Target
        Cost(i) = Cost(i) + Desired_Margins.GM.Weight*((margins.GM(i) - Desired_Margins.GM.Target)/Desired_Margins.GM.Target)^2;
    end
end

% PM
if Desired_Margins.PM.Weight > 0
    if margins.PM(i) < Desired_Margins.PM.Target
        Cost(i) = Cost(i) + Desired_Margins.PM.Weight*((margins.PM(i) - Desired_Margins.PM.Target)/Desired_Margins.PM.Target)^2;
    end
end
% BW
if Desired_Margins.BW.Weight > 0
    if margins.BW(i) < Desired_Margins.BW.Target
        Cost(i) = Cost(i) + Desired_Margins.BW.Weight*((margins.BW(i) - Desired_Margins.BW.Target)/Desired_Margins.BW.Target)^2;
    end
end


% ETF UB

ETF_Mag = 20*log10(abs(squeeze(bode(margins.ETF_DD{i}))));% ATTENTITOOONNNN 

for ix = 1:length(ETF_Mag)    
    if ETF_Mag(ix) > Desired_Margins.ETFUB.TargetVec(ix)
        Cost(i) = Cost(i) + Desired_Margins.ETFUB.WeightVec(ix)*((ETF_Mag(ix) - Desired_Margins.ETFUB.TargetVec(ix))/Desired_Margins.ETFUB.TargetVec(ix))^2;
    end
end
    

% OL UB
OL_Mag = 20*log10(abs(squeeze(bode(margins.OL_DD{i}))));% ATTENTITOOONNNN

for ix = 1:length(OL_Mag)    
    if OL_Mag(ix) > Desired_Margins.OLUB.TargetVec(ix)
        Cost(i) = Cost(i) + Desired_Margins.OLUB.WeightVec(ix)*((OL_Mag(ix) - Desired_Margins.OLUB.TargetVec(ix))/Desired_Margins.OLUB.TargetVec(ix))^2;
    end
end
end


Total_Cost = sum(Cost);

if any(margins.GM) > 100 ||  any(margins.PM > 150) || any(margins.PM) < 1 || any(isnan(margins.BW)) 
    Total_Cost = 1e6  ;
end