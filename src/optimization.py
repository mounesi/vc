from vibration import Const, Plant, Margin, Controller, ControlParam
from cost import Cost 
from scipy.optimize import minimize, Bounds
import sys
import time


def IO(x):
    myctparam.i += 1

    
    var_bool = myctparam.xlimit(x)
    if (var_bool == False):
        total_cost = Margin.MAXIMUM 
        myctparam.xlog(x, myctparam.i , total_cost, var_bool)
        print(f'ITERATION = {myctparam.i}\t\t***   TOTAL COST = {total_cost}\t\t*** condition out of boundary')
        return total_cost

    ctfrd = myct.run(x)
    try:
        total_cost = mycost.run(ctfrd)
    except Exception as e:
        print(f'x == {x}')
        raise e

    myctparam.xlog(x, myctparam.i , total_cost, var_bool)
    print(f'ITERATION = {myctparam.i}\t\t***   TOTAL COST = {total_cost}')
    return total_cost

    

mypl    = Plant()
mypl.run(Const.PLANT_PATH)

mymrg   = Margin()
mymrg.run(mypl.freqhz, mypl.freqhzunit)

# IN THIS SCRIPT
mycost  = Cost(mymrg, mypl)   
myct    = Controller(mypl.freq)
myctparam = ControlParam()
xparam  = myctparam.xinitial(4)
#iter_num = myctparam.i
#mybound = Bounds(Const.XMIN, Const.XMAX, keep_feasible=False)
#xu      = minimize(fun = IO, x0= ControlParam.x_notch4 , method ='COBYLA', options={'rhobeg': 1.0, 'maxiter': 20, 'disp': True, 'catol': 0.0002})

Const.OPTMETHOD = 'Nelder-Mead' 

tstart = time.monotonic()
xu      = minimize(fun = IO, x0= xparam , method = Const.OPTMETHOD, options={'rhobeg': 1.0, 'maxiter':100 , 'disp': True, 'catol': 0.0002})
tend   = time.monotonic()

dt = tend - tstart
myctparam.xfinal(xu.x,myctparam.i ,dt,xu.fun)
"""
Nelder-Mead 
Powell 
CG 
BFGS 
Newton-CG 
L-BFGS-B  ***
TNC  ***
COBYLA 
SLSQP  ***
trust-constr
dogleg
trust-ncg
trust-exact
trust-krylov
"""
