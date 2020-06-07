function C_separate_z = control_separate_builder(x,T)

 %x0 = Control_Knobs.x0 ; 
 c_p = c2d(tf(x(1),1),T,'matched'); 
 c_i = c2d(tf(x(2),[1 0]),T, 'matched'); 
 %c_i.num{1,1}(1,2) = c_i.num{1,1}(1,2)+.002 ; 
 
 
 low_pas_TF_z = c2d(tf([x(3)],[1 x(3)]),T,'matched');
 

notch_length = evalin('base','notch_length');
Notch_matrix = zeros(notch_length,3) ; 

for j = 1 : 3*notch_length ; % because of the 3 variables
    Notch_matrix(j) = x(j+3); 
end
%Notch_matrix
D = Notch_matrix(:,1);
W = Notch_matrix(:,2);
F= Notch_matrix(:,3);


for i = 1:notch_length; 
     C_separate_z.Notch{i} = c2d(NotchTFs(D(i),W(i),F(i),F(i)),T,'matched');
     
end

C_separate_z.p = c_p ; 
C_separate_z.i = c_i ; 
C_separate_z.lowP = low_pas_TF_z;

%max(pole(C_separate_z.pi), pole(C_separate_z.lowP), C_separate_z.Notch{1}, C_separate_z.Notch{2}, C_separate_z.Notch{3}, C_separate_z.Notch{4}, C_separate_z.Notch{5}, C_separate_z.Notch{6})
max(abs(pole(C_separate_z.p)))
max(abs(pole(C_separate_z.i)))
max(abs(pole(C_separate_z.lowP)))
max(abs(pole(C_separate_z.Notch{1})))
max(abs(pole(C_separate_z.Notch{2})))
max(abs(pole(C_separate_z.Notch{3})))
max(abs(pole(C_separate_z.Notch{4})))
% max(abs(pole(C_separate_z.Notch{5})))
% max(abs(pole(C_separate_z.Notch{6})))
%figure; bode(controller_z)
% NotchTFs(D,W,FreqNum,FreqDen)

% D: Notch Depth (dB)
% W: Notch Width (Hz)
% FreqNum: Notch numerator frequency (Hz)
% FreqDen: Notch denominator frequency (Hz)