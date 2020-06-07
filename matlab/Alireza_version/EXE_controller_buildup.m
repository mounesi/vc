%% EXE_Beam code developed by Alireza Mounesisohi, San Jose State University Student
%% intializing and reading data

close all
[Plants, Desired_Margins, LB, UB, x0, frdfreq, Num_Plants, T,notch_length] = read_plants_targets_knobs(); 

%x0 = [1.93668629488918,10.2595547301294,19.1176567204009,21.1564314107106,21.1846196926659,7.28727975912903,7.09369177916801,9.98794306200078,10.2912339088769,2.91785747500258,3.04175476725767,4.32126623446548,4.50353172840543,26.6637329799472,26.9121285043219];
%x0 = [1.92616983536746,10.2363791605701,18.8443310513576,21.3690045736779,21.7018275625564,7.42233090695724,7.10456210720496,9.90517726220625,10.3536116267041,2.90619449637575,3.04485369301464,4.26355764872520,4.39160711493909,27.4127482589280,27.4982652180209]; 
%x0 = [1.92882479916862,10.2506423874309,18.8704203842981,21.3980466373714,22.2747199617238,7.43265514460678,7.11441875359134,9.91873442676810,10.3403999565188,2.90802748404730,3.04357384816856,4.26091605738255,4.39523506151710,27.3,76.6] ; 
x0 = [2.02709881757056,10.2461559295746,18.8631630934152,22.4628628060177,24.5903310202867,7.43346453733955,7.12093283554538,9.90976871574991,10.3464110054736,2.91177390575317,3.04404473356926,4.25766789384977,4.38977695080234,27.2872417429954,80.3002160575463] ;

Num_Plants = 3;

C_z = control_builder(x0,T);
simulate_plots(C_z , x0);
C_separt = control_separate_builder(x0,T);
margins = margin_calculator(C_z, Plants)

f0 = cost_at_margin(x0)
%% fminsearch
options = optimset('MaxFunEvals',20,'Display','iter');
[x_opt f_opt] = fminsearch_con('cost_at_margin',x0,LB,UB,1e20,options);


C_z = control_builder(x_opt,T);
max(abs(pole(C_z)))
simulate_plots(C_z, x_opt);
C_separt = control_separate_builder(x_opt,T);

%% Final Control Values
CNT_N = C_z.num{1, 1}
CNT_D = C_z.den{1, 1}