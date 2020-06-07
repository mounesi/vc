function margins = margin_cal(C_z, Plants); 

Num_Plants = evalin('base','v.num_plants') ; 

for i = 1: Num_Plants; 
    margins.OL_DD{i} = Plants{i}*C_z; 
    margins.CL_DD{i} = margins.OL_DD{i}/(1+margins.OL_DD{i}); 
    margins.ETF_DD{i} = 1/(1+margins.OL_DD{i}); % sensitivity
    [margins.GM(i) ,margins.PM(i) ,margins.Wgm(i), margins.BW(i)] = margin(margins.OL_DD{i}); 
    margins.BW(i) = margins.BW(i)/2/pi;
end
