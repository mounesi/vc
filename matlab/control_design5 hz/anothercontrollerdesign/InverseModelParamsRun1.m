%% Find Hysteresis weights of Polynomial Function

x = [0:0.01:100];
p1 = 2.4705e-08;
p2 = 5.4493e-05;
p3 = 0.0041746;
y = p1*x.^3 + p2*x.^2 + p3*x;
r_scale = [0 .02 .04 .06 .08 .1 .12 .14 .16 .18 .2 .22 .24 .28 .32 .36 .40 .45 .50 .55 .6 .65 .7 .75 .8 .9]; % Threshold percentages of max input
Vmax = max(x); % read max input
r = r_scale*Vmax; % scale threshold by max Vmax
y_thresh  = zeros(1,length(r));
for i = 1:length(r)
    y_thresh(i) = p1*r(i).^3 + p2*r(i).^2 + p3*r(i);
end
slope = zeros(1,length(r));
for i = 1:(length(r)-1)
    slope(i) = (y_thresh(i+1)-y_thresh(i))/(r(i+1)-r(i));
end
slope(length(r)) = (max(y) - y_thresh(length(r)))/(max(x)-r(end));
w = zeros(1,length(r));
w(1) = slope(1);
for i = 2:length(r)
   w(i) = slope(i)-slope(i-1);
end

%% Calculate inverse hysteresis wieghts and thresholds.

r_inv = zeros(1,length(r));
w_inv = zeros(1,length(r));
for i = 1:length(r)
    for j = 1:i
        r_inv(i) = r_inv(i)+(r(i)-r(j))*w(j);
    end
end
w_inv(1) = 1/w(1);
m = 0;
n = 0;
for i = 2:length(r)
    for j = 1:i
        m = m + w(j);
    end
    for j = 1:(i-1)
        n = n + w(j);
    end
    w_inv(i) = -w(i)/(m * n);
    n = 0;
    m = 0;
end
