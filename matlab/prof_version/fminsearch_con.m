function [xopt, fopt] = fminsearch_con(func_name,x0,LB,UB,w,options)

% This funciton carries out fminsearch with Lower and Upper bound constraints. 
% For best results, do not include "zero" in any of the parameter bounds.

% Parameters
LB(find(LB == 0)) = -1e-6; % In case LB includes 0
UB(find(UB == 0)) = 1e-6;  % In case UB includes 0
w1 = 1e20;                 % In case w is not provided.

% Code
if nargin == 4
    w = w1;
    [xopt, fopt] = fminsearch(@new_cost_func,x0);
elseif nargin == 5
    [xopt, fopt] = fminsearch(@new_cost_func,x0);
elseif nargin == 6
    [xopt, fopt] = fminsearch(@new_cost_func,x0,options);
else
    xopt = [];
    fopt = [];
    disp('Not enough input arguments')
end

    function cost = new_cost_func(x)
        cost = feval(func_name,x);
        indLB = find(x<LB);
        indUB = find(x>UB);
        if any(indLB)
            penLB = w*((x(indLB)-LB(indLB))./LB(indLB)).^2;
            cost = cost + penLB;
        end
        if any(indUB)
            penUB = w*((UB(indUB)-x(indUB))./UB(indUB)).^2;
            cost = cost + penUB;
        end
    end

end
