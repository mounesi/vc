function margins = margin_calculator(C_z,Plants); 

frdfreq = evalin('base','frdfreq') ; 
Num_Plants = evalin('base','Num_Plants') ; 


for i = 1: Num_Plants; 
    margins.OL_DD{i} = Plants{i}*C_z;
    margins.CL_DD{i} = margins.OL_DD{i}/(1+margins.OL_DD{i}); 
    margins.ETF_DD{i} = 1/(1+margins.OL_DD{i}); % sensitivity
    [margins.GM(i) ,margins.PM(i) ,margins.Wgm(i), margins.BW(i)] = margin(margins.OL_DD{i});
    margins.BW(i) = margins.BW(i)/2/pi;
    
    
    % BW
%     ind2 = find(abs(margins.OL_DD{1, i}.ResponseData)<1,1);
%     ind1 = ind2 -1 ;
%     f2 = frdfreq(ind2);
%     f1 = frdfreq(ind1);
%     y2 = abs(margins.OL_DD{1, i}.ResponseData(:,:,ind2));
%     y1 = abs(margins.OL_DD{1, i}.ResponseData(:,:,ind1));
%     m = (y2 - y1)/(f2-f1)   ;
% 
%     margins.BW(i) = -1/m*(y2 - 1) + f2;
    
end

