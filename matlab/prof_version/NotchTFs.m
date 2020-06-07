function Notchs = NotchTFs(D,W,FreqNum,FreqDen)

% D: Notch Depth (dB)
% W: Notch Width (Hz)
% FreqNum: Notch numerator frequency (Hz)
% FreqDen: Notch denominator frequency (Hz)

zeta1 = 2*W*10^(-D/20)/(FreqNum + FreqDen);
zeta2 = 2*W/(FreqNum + FreqDen);

Notchs = FreqDen^2/FreqNum^2*(tf([1 4*zeta1*pi*FreqNum (2*pi*FreqNum)^2], [1 4*zeta2*pi*FreqDen (2*pi*FreqDen)^2]));