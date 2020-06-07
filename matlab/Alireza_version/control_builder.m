function C_z = control_builder(x,T)

notch_length = evalin('base','notch_length');
 
%%
 c_p = c2d(tf(x(1),1),T,'matched')
 c_i = c2d(tf(x(2),[1 0]),T, 'matched')
 piTF_z = c_i + c_p                            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Major Change
 low_pass_TF_s = tf([x(3)],[1 x(3)])
 low_pas_TF_z = c2d(tf([x(3)],[1 x(3)]),T,'matched')
 ControllerTF_z = low_pas_TF_z * piTF_z 

 %%
Notch_matrix = zeros(notch_length,3) ; 

for j = 1 : 3*notch_length ; % because of the 3 variables
    Notch_matrix(j) = x(j+3); 
end

%Notch_matrix
D = Notch_matrix(:,1);
W = Notch_matrix(:,2);
F= Notch_matrix(:,3);

for i = 1:notch_length; 
     ControllerTF_z = ControllerTF_z*c2d(NotchTFs(D(i),W(i),F(i),F(i)),T,'matched');
     %max(abs(pole(ControllerTF_z)))
end
C_z = ControllerTF_z

%figure; bode(controller_z)
% NotchTFs(D,W,FreqNum,FreqDen)

% D: Notch Depth (dB)
% W: Notch Width (Hz)
% FreqNum: Notch numerator frequency (Hz)
% FreqDen: Notch denominator frequency (Hz)