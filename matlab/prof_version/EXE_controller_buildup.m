%% EXE_Beam code developed by Alireza Mounesisohi, San Jose State University Student
%% intializing and reading data

close all
[Plants, Desired_Margins, LB, UB, x0, frdfreq, Num_Plants, T,notch_length] = read_plants_targets_knobs(); 

% x0 = [2.83106591708333,6.47242564604546,25.7569429708707,19.2878410320475,34.5038103686915,34.4184728703311,19.5530099727454,11.1196550222603,4.96520694009994,4.06632827074190,3.88133417672812,9.24860584635203,4.67350848734160,4.20882784046413,27.3465612461372,76.6365446127718];

x0 = [0.377520219664617,5.00587573112262,9.82945497920471,58.7468860396891,12.0530137360793,19.9999685699908,13.3404315991752,2.56030938354148,4.08624297594041,3.36815967638889,4.07475559435954,27.3295864785435,77.3707883895904];

Num_Plants = 3;

C_z = control_builder(x0,T);
simulate_plots(C_z , x0);
C_separt = control_separate_builder(x0,T);
margins = margin_calculator(C_z, Plants)

f0 = cost_at_margin(x0)
%% fminsearch
options = optimset('MaxFunEvals',4000,'Display','iter');
[x_opt f_opt] = fminsearch_con('cost_at_margin',x0,LB,UB,1e20,options);


C_z = control_builder(x_opt,T);
max(abs(pole(C_z)))
simulate_plots(C_z, x_opt);
C_separt = control_separate_builder(x_opt,T);

%% Final Control Values
CNT_N = C_z.num{1, 1}
CNT_D = C_z.den{1, 1}