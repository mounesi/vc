function C_z = contr_build(x,T)

 %x0 = Control_Knobs.x0 ; 
 piTF = tf([x(1) x(2)],[1 0]); 
 low_pas_TF = tf([x(3)],[1 x(3)]);
 ControllerTF = c2d(low_pas_TF * piTF,T,'matched') ;  
%  notch_1 = NotchTFs(x(4),x(7),x(10),x(10));
%  notch_2 = NotchTFs(x(5),x(8),x(11),x(11));
%  notch_3 = NotchTFs(x(6),x(9),x(12),x(12));
% 
% ContTF_s = piTF*low_pas_TF*notch_1*notch_2*notch_3 ; 

% Considering the three initial knobs for the lowpass and pi then

%x= Control_Knobs.x0 ; 

c = evalin('base','c');
notch_length = c.notch_length;

Notch_matrix = zeros(notch_length,3) ; 

for j = 1 : 3*notch_length ; % because of the 3 variables
    Notch_matrix(j) = x(j+3); 
end

D = Notch_matrix(:,1);
W = Notch_matrix(:,2);
F= Notch_matrix(:,3);

for i = 1:notch_length; 
     ControllerTF = ControllerTF*c2d(NotchTFs(D(i),W(i),F(i),F(i)),T,'matched');
end
C_z = ControllerTF;

%figure; bode(controller_z)
% NotchTFs(D,W,FreqNum,FreqDen)

% D: Notch Depth (dB)
% W: Notch Width (Hz)
% FreqNum: Notch numerator frequency (Hz)
% FreqDen: Notch denominator frequency (Hz)