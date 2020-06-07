from vibration import Const, Margin, Plant, Controller, ControlParam
from scipy import signal
import control as ct
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

def x_get(): 
    myctparam = ControlParam()
    notch_number = 4
    line_number  = 1000
    ext_meth    = 'last' # 'io' or 'log' or 'last'
    
    if ext_meth == 'io': 
        x = myctparam.xioline (notch_number = notch_number, line_number = line_number)
    if ext_meth == 'log':
        x = myctparam.xlogline(notch_number = notch_number, line_number = line_number)
    if ext_meth == 'last':
        x = myctparam.xinitial(notch_number)
 
    return x


mypl = Plant()
mypl.run(Const.PLANT_PATH)
"""
self.name       = IMPORTED
self.frd        = IMPORTED
self.freq       = IMPORTED
self.ts         = IMPORTED
self.timeunit   = IMPORTED
self.frequnit   = IMPORTED
self.length     = None
self._rd        = IMPORTED
self.freqhz     = None
self.freqhzunit = None
"""

mymrg = Margin()
mymrg.run(mypl.freqhz, mypl.freqhzunit)
"""
self.gmt        = gmt
self.gmw        = gmw
self.pht        = pht
self.phw        = phw
self.bwt        = bwt
self.bww        = bww
self.etfub_freq = etfub_freq
self.etfub_t    = etfub_t
self.etfub_w    = etfub_w
self.olub_freq  = olub_freq
self.olub_t     = olub_t
self.olub_w     = olub_w
self.etfub_tv   = []
self.etfub_wv   = []
self.olub_tv    = []
self.olub_wv    = []
"""

xparam  = x_get()
print(xparam)
print(type(xparam))
myct= Controller(mypl.freq)
myct.run(xparam)
"""
self.controller_structure   = Const.CONTROLLER_STRUCTURE
self.kp                     = Const.kp
self.ki                     = Const.ki
self.kd                     = Const.kd
self.b                      = Const.bden
self.notchvars              = Const.NOTCHVARS
self.discrete_ts            = Const.DISCRETE_TS
self.discrete_method        = Const.DISCRETE_METHOD
self.pi                    = None
self.notch                  = None
self.lp                     = None
self.controller_s           = None
self.controller_z           = None
self.eval_freq_rad          = None
self.controller_frd         = None
"""
def plt_pl():
    ct.bode(mypl.frd, mypl.freq)    

def plt_ol():
    ol = []
    for pl in mypl.frd:
        ol.append(pl*myct.controller_frd)
    ct.bode(ol, mypl.freq)    

def plt_etf():
    etf = []
    for pl in mypl.frd:
        ol = pl*myct.controller_frd
        etf.append(ol/(1+ol))
    ct.bode(etf, mypl.freq) 
    
    
def plt_layed_ol():



    ol = []    
    for pl in mypl.frd:
        ol.append(pl*myct.controller_frd)  
    
    mag_abs = []
    phase_rad = []
    omega_res_rad_s = []
    freq_hz = []
    for i in range(mypl.length):
        rsp_mag_phase_omega = ol[i].freqresp(mypl.freq)
        print(rsp_mag_phase_omega)
        mag_abs.append(list(rsp_mag_phase_omega[0][0][0]))
        phase_rad.append(list(rsp_mag_phase_omega[1][0][0]))
        omega_res_rad_s.append(list(rsp_mag_phase_omega[2]))
        freq_hz.append(list(rsp_mag_phase_omega[2]/2/np.pi))

    plt.figure
    ax = plt.gca()

    for i in range(mypl.length):
        plt.plot(freq_hz[i], mag_abs[i])
    # [xmin,xmax], [ymin,ymax])

    
    xmin = 0
    xmax = mymrg.olub_freq_hz[0]
    ymin = db2abs(mymrg.olub_t_db[0])
    ymax = db2abs(mymrg.olub_t_db[0])
    
    xmin2 = mymrg.olub_freq_hz[0]
    xmax2 = mymrg.olub_freq_hz[1]
    ymin2 = db2abs(mymrg.olub_t_db[1])
    ymax2 = db2abs(mymrg.olub_t_db[1])
    """
    self.etfub_freq_hz = etfub_freq_hz
        self.etfub_t_db    = etfub_t_db
        self.etfub_w       = etfub_w
        # open loop
        self.olub_freq_hz  = olub_freq_hz
        self.olub_t_db     = olub_t_db
        self.olub_w        = olub_w

    """
    l1 = mlines.Line2D([xmin,xmax], [ymin,ymax])
    ax.add_line(l1)
    
    l2 = mlines.Line2D([xmin2,xmax2], [ymin2,ymax2])
    ax.add_line(l2)
    
    l3 = mlines.Line2D([xmin2,xmin2], [ymin,ymin2])
    ax.add_line(l3)

    ax.set_yscale('log')
    #newline(p1,p2)
    plt.ylabel('magnitude')
    plt.xlabel('frequency')
    plt.show

def db2abs(x_db):
    return 10**(x_db/20)

def plt_layed_eft():
    pass
    
    
    
if __name__ == '__main__': 
#    plt_pl()
#    plt_ol()
#    plt_etf()
    plt_layed_ol()
#    plt_layed_etf()
    





