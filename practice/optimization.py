

from scipy.optimize import minimize, Bounds
import numpy as np

c = 2 

class PracOpt(object):
    b = 2
    def __init__(self):
        self.a = 2

    x0 = np.array([5, 4, 1])

    xmin = [ -20, -20, -7 ] 
    xmax = [  20,  20,  20 ]

    
    def banana(x): 
        return (x[0]-1)**2 + (x[1]+2)**2 + x[2]
    mybound = Bounds(xmin, xmax, keep_feasible=False)

    xu = minimize(fun = banana, x0= x0, method ='TNC', bounds = mybound)

    print('xu is : ')
    print(xu.x)
    print('minval is: ')
    print(xu.fun)


myopt1 = PracOpt()
