#import numpy as np

import pickle
import control as ct
import numpy as np
import csv

class Const(object): 
    """
    this class is 
    static
    contains
    contr  const initial
    contr  const bounds 
    """
    # CONST CONSTANTS
    # MARGINS     
    GAIN_MARGIN_TARGET_DB   = 4  # db
    GAIN_MARGIN_WEIGHT      = 1
    
    PHASE_MARGIN_TARGET_DEG = 40 # degree
    PHASE_MARGIN_WEIGHT     = 1
    
    BANDWIDTH_TARGET_HZ     = 3  # hz
    BANDWIDTH_WEIGHT        = 1
    
    ETFUB_FREQ_HZ       = [4.1, 250]  # hz
    ETFUB_TARGET_DB     = [8, 2]    # db
    ETFUB_WEIGHT        = [10, 10]
    
    OLUB_FREQ_HZ        = [4.1, 250]  # hz 
    OLUB_TARGET_DB      = [40, -10] # db
    OLUB_WEIGHT         = [10, 10]


    # CONTROLLER PARAMS 
    kp          = 2
    KP_MIN      = 1E-6
    KP_MAX      = 1E6
    ki          = 10
    KI_MIN      = 1E-6
    KI_MAX      = 1000
    KI_ALPHA    = 1E-10
    
    bden        = 20
    BDEN_MIN    = 1E-6
    BDEN_MAX    = 100

    x_default   = [kp, ki, bden]
    XMIN        = [KP_MIN, KI_MIN, BDEN_MIN] 
    XMAX        = [KP_MAX, KI_MAX, BDEN_MAX]


    nnf = 4  # number of notches to be used 
    if nnf:
        nd_v              = [ 20, 20, 7, 7, 1.5, 1]
        NDEPTH_V_MIN      = [ 1, 1, 1, 1, 1, 1]
        NDEPTH_V_MAX      = [ 25, 25, 25, 25, 25, 25]

        nw_v              = [10, 10, 3, 3, 1.5, 1.1]
        NWIDTH_V_MIN      = [1, 1, 1, 1, 1, 1]
        NWIDTH_V_MAX      = [20, 20, 20, 20, 20, 20]

        nf_v_hz           = [4.35,  5, 27, 27.6, 76.7, 165]
        NFREQ_V_HZ_MIN    = [1, 1, 1, 1, 1, 1]
        NFREQ_V_HZ_MAX    = [250, 250, 250, 250, 250, 250]
   
        xnotch     = nd_v[:nnf]         + nw_v[:nnf]         + nf_v_hz[:nnf]
        XMINnotch  = NDEPTH_V_MIN[:nnf] + NWIDTH_V_MIN[:nnf] + NFREQ_V_HZ_MIN[:nnf]
        XMAXnotch  = NDEPTH_V_MAX[:nnf] + NWIDTH_V_MAX[:nnf] + NFREQ_V_HZ_MAX[:nnf]
  
        x_default += xnotch 
        XMIN      += XMINnotch
        XMAX      += XMAXnotch
    
    DISCRETE_TS       = 0.002  
    DISCRETE_METHOD1   =  'bilinear'
    DISCRETE_METHOD2   =  'matched' 
                        
    CONTROLLER_STRUCTURE    = 'pi_b_6n'
    ITERATION    = 200

    # DIRECTORY PATHS
    BASE_PATH           = '/home/ali/p/beam'
    RESULT_PATH         = BASE_PATH + '/result'
    PLANT_PATH          = BASE_PATH + '/plant/TFMAIN4.pkl'
    PARAM_PATH          = BASE_PATH + '/controlparam'


    x_notch4_initial = [.2,.2,18.8631630934152,22.4628628060177,24.5903310202867,7.43346453733955,7.12093283554538,9.90976871574991,10.3464110054736,2.91177390575317,3.04404473356926,4.25766789384977,4.38977695080234,27.2872417429954,80.3002160575463] # for 40 db 

    """
    xlog:[0.1972467396384788, 0.1998707020803352, 18.863162851592133, 24.9931968456825, 24.06001205110739, 7.433464537212738, 7.1209328355216, 9.909768474996355, 10.34641096602963, 2.9117739054464655, 4.0440446593217585, 4.257664495553204, 4.389766968225762, 30.287241669011152, 80.3002158367048]:i:95:e:1.2556068533398284:b:crashed
    """


class ControlParam(object):
    def __init__(self): 
        self.x  = None
        self.nn = None
        self.i  = None  # iteration 
        self.t  = None
        self.e  = None
        self.f_path = None

    def xinitial(self,n):
        self.nn = n
        self.f_path = Const.PARAM_PATH + f'/x40_notch{self.nn}.csv'
        with open(self.f_path,'r', newline = '') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=':', quotechar='|')
            for row in spamreader:
                pass
        self.x = eval(row[1]) 
        self.i = int(row[3])
        self.t = float(row[5])
        self.e = float(row[7])
        return self.x


    def xioline(self,notch_number, line_number):
        self.nn = notch_number
        self.ln = line_number
        
        self.f_path = Const.PARAM_PATH + f'/x40_notch{self.nn}.csv'
        with open(self.f_path,'r', newline = '') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=':', quotechar='|')
            row_c = 0 
            for row in spamreader:
                row_c += 1
                if row_c == self.ln:
                    break

        self.x = eval(row[1]) 
        self.i = int(row[3])
        self.t = float(row[5])
        self.e = float(row[7])

        print(self.i)
        return self.x

    def xlogline(self, notch_number, line_number):
        self.nn = notch_number
        self.ln = line_number
        self.log_path = Const.PARAM_PATH + f'/xlog_40_notch{self.nn}.csv'
        with open(self.log_path,'r', newline = '') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=':', quotechar='|')
            row_c = 0 
            for row in spamreader:
                row_c += 1
                if row_c == self.ln:
                    break

        self.x = eval(row[1]) 
        self.i = int(row[3])
        self.e = float(row[5])
        self.b = row[7]

        print(self.i)
        return self.x

    def xlog(self, xlog, iterglobal, error,var_bool): 
        self.log_path = Const.PARAM_PATH + f'/xlog_40_notch{self.nn}.csv'
        self.error = error
        self.log_file =  open(self.log_path, mode = 'a')
        myfile = csv.writer(self.log_file, delimiter=':', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        myfile.writerow(['xlog', list(xlog), 'i',iterglobal,'e', self.error, 'b', var_bool])


    def xfinal(self,xfinal,iterglobal, tlocal,errorfinal):
        self.log_file.close()
        tglobal = self.t + tlocal
        self.e  = errorfinal
        with open(self.f_path, mode = 'a') as e_file:
            myfile = csv.writer(e_file, delimiter=':', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            myfile.writerow(['x', list(xfinal), 'i',iterglobal, 't',tglobal, 'e', self.e])


    def xlimit(self,x):
        var_bool = True
        for i in range(len(x)):
            var_bool = var_bool and (Const.XMIN[i]<x[i]<Const.XMAX[i]) 
        
        return var_bool




class Margin(object): 
    """
    This class is 
    init input > constant margins 
    run  input > frequency spectrum 
    output> complete margin constans
    """

    MAXIMUM = float(1000000)

    def __init__(self, 
                gmt_db          = Const.GAIN_MARGIN_TARGET_DB,
                gmw             = Const.GAIN_MARGIN_WEIGHT,
                pht_deg         = Const.PHASE_MARGIN_TARGET_DEG,
                phw             = Const.PHASE_MARGIN_WEIGHT,
                bwt_hz          = Const.BANDWIDTH_TARGET_HZ,
                bww             = Const.BANDWIDTH_WEIGHT,
                etfub_freq_hz   = Const.ETFUB_FREQ_HZ,
                etfub_t_db      = Const.ETFUB_TARGET_DB,
                etfub_w         = Const.ETFUB_WEIGHT,
                olub_freq_hz    = Const.OLUB_FREQ_HZ,
                olub_t_db       = Const.OLUB_TARGET_DB,
                olub_w          = Const.OLUB_WEIGHT,
                ): 

        # MARGIN INIT INPUT
        # gain margin
        self.gmt_db     = gmt_db
        self.gmt        = 10**(gmt_db/20) # abs 
        self.gmw        = gmw
        # phase margin
        self.pht_deg    = pht_deg
        self.pht        = pht_deg*np.pi/180 # rad
        self.phw        = phw
        # bandwidth
        self.bwt_hz     = bwt_hz
        self.bwt        = bwt_hz*2*np.pi # rad/s
        self.bww        = bww
        # error tf
        self.etfub_freq_hz = etfub_freq_hz
        self.etfub_t_db    = etfub_t_db
        self.etfub_w       = etfub_w
        # open loop
        self.olub_freq_hz  = olub_freq_hz
        self.olub_t_db     = olub_t_db
        self.olub_w        = olub_w
        
        # MARGIN OUTPUT
        self.etfub_t_dbv   = []
        self.etfub_wv      = []
        self.olub_t_dbv    = [] 
        self.olub_wv       = [] 

    def run(self, freq, frequnit):
        
        # MARGIN INPUT RUN
        freq1 = freq
        freq2 = freq

        if frequnit == 'hz':
            etfub_t_dbv = []
            etfub_wv = []
            for j, et_can in enumerate(self.etfub_freq_hz):
                for i, freq_can in enumerate(freq1):
                    if freq_can <= et_can: 
                        etfub_t_dbv.append(self.etfub_t_db[j])
                        etfub_wv.append(self.etfub_w[j])
                    else: 
                        freq1 = freq1[i:]
                        break

            olub_t_dbv = []
            olub_wv = []
            for j, ol_can in enumerate(self.olub_freq_hz):
                for i, freq_can in enumerate(freq2):
                    if freq_can <= ol_can:
                        olub_t_dbv.append(self.olub_t_db[j])
                        olub_wv.append(self.olub_w[j])
                    else: 
                        freq2 = freq2[i:]
                        break


            self.etfub_t_dbv = etfub_t_dbv  
            self.etfub_tv    = [10**(item/20) for item in etfub_t_dbv]
            self.etfub_wv    = etfub_wv

            self.olub_t_dbv  = olub_t_dbv
            self.olub_tv     = [10**(item/20) for item in etfub_t_dbv]
            self.olub_wv     = olub_wv
        

        else: 
            print('convert the unit to hz and try again')



class Plant(object):

    """
    This class is to read the plants: 
    init input > None
    run input  > plant_path
    run output > all the plants with informations
    """
    def __init__(self):
            

        # PLANT OUTPUT
        self.name       = [] 
        self.frd        = []
        self.freq       = None
        self.ts         = None
        self.timeunit   = None
        self.frequnit   = None
        self.length     = None
        self._rd        = [] 
        self.freqhz     = None
        self.freqhzunit = None

    def run(self, plant_path):
        
        # PLANT RUN INPUT
        self.plant_path = plant_path

        infile  = open(self.plant_path ,'rb')
        pl_file = pickle.load(infile)
        infile.close()

        """
            tf_frd[k] = (
                        {'name'     : tf[k]['name']},
                        {'frdtf'    : frd_re_omega_complex},
                        {'freqrad'  : freq_rad_array},
                        {'rd'       : rd_list},
                        {'ts'       : tf[k]['ts']},
                        {'timeunit' : tf[k]['timeunit']},
                        {'frequnit' : tf[k]['frequnit']}
                        )
        """
#        for k in range(13): 
        for k in [7, 10, 11]: 
            self.name.append(   pl_file[k][0]['name'])
            self.frd.append(    pl_file[k][1]['frdtf']) 
            self._rd.append(    pl_file[k][3]['rd'])
        
        # since all the frequencies, ts, timeunit, frequnit, are the same
        k = 5 
        self.freq       = pl_file[k][2]['freqrad']
        self.ts         = pl_file[k][4]['ts']
        self.timeunit   = pl_file[k][5]['timeunit']
        self.frequnit   = pl_file[k][6]['frequnit']
        self.freqhz     = self.freq/np.pi/2
        self.freqhzunit = 'hz'
        
        self.length     = len(self.frd)
        self.freqlen    = len(self.freq)

    def plot(self):

        for k in range(self.length):
            ct.bode_plot(self.frd[k], self.freq, dB = True)
    


class Controller(object): 
    """
    This class is dynamic
    init input > Const Controller
    run  input > eval_freq from plant
    output frd controller
    """

    
    def __init__(self,
        eval_freq_rad, 
        discrete_ts            = Const.DISCRETE_TS,
       # discrete_method        = Const.DISCRETE_METHOD
        ): 

        # CONTROLLER INPUT
        self.discrete_ts            = discrete_ts
       # self.discrete_method        = discrete_method
        self.eval_freq_rad          = eval_freq_rad
        self.nnf                    = Const.nnf        
        # CONTROLLER OUTPUT
        

    def run(self,x): 

        self.x   = x
        self.kp  = x[0] 
        self.ki  = x[1]
        self.b   = x[2]
        self.pi  = None
        self.lp  = None
        if self.nnf:
            n = 3 
            self.nd_v    = x[n: n + self.nnf] 
            self.nw_v    = x[n + self.nnf:n + 2*self.nnf]
            self.nf_v_hz = x[n + 2*self.nnf:]  
            self.notchf   = None

#       
#        print(self.nd_v)
#        print(self.nw_v)
#        print(self.nf_v_hz)
        
        self.controller_s   = None 
        self.controller_z   = None
        self.controller_frd = None

        self.pitf()
        self.piz = Controller.s2d_tf(self.pi\
                           , self.discrete_ts, Const.DISCRETE_METHOD1 )
        self.lptf()
        self.lpz = Controller.s2d_tf(self.lp\
                           , self.discrete_ts, Const.DISCRETE_METHOD2 )
        
        self.controller_z = self.piz* self.lpz
        self.controller_s = self.pi * self.lp  
        
        if self.nnf:
            self.notchtf()
            self.notchz = Controller.s2d_tf(self.notchf\
                           , self.discrete_ts, Const.DISCRETE_METHOD2 )
            self.controller_s *= self.notchf  
            self.controller_z *= self.notchz

        self.controller_frd = Controller.d2frd_tf(self.controller_z\
                            , self.eval_freq_rad)

        return self.controller_frd

    @staticmethod
    def s2d_tf(sys,ts,method):
        return sys.sample(ts, method) 

    @staticmethod
    def d2frd_tf(sys_z, freq):
        return ct.FRD(sys_z, freq)
    
    def pitf(self): 
        self.pi    = ct.tf([self.kp, self.ki], [1, Const.KI_ALPHA])

    def lptf(self):
        self.lp  = ct.tf([self.b], [1, self.b])

    @staticmethod
    def notch_one(d, w, fnum, fden):
        """
        d: Notch Depth (dB)
        w: Notch Width (Hz)
        fnum: Notch numerator frequency (Hz)
        fden: Notch denominator frequency (Hz)
        """
        z1  = 2*w*10**(-d/20)/(fnum + fden)
        z2  = 2*w/(fnum + fden)
        return  fden**2/fnum**2*(ct.tf( [1, 4*z1*np.pi*fnum,(2*np.pi*fnum)**2], \
                                        [1, 4*z2*np.pi*fden,(2*np.pi*fden)**2]))


    def notchtf(self):
        notch_can   = ct.tf([1],[1])
        for i in range(self.nnf):
            d   = self.nd_v[i]
            w   = self.nw_v[i]
            f   = self.nf_v_hz[i]
            notch_now   = Controller.notch_one(d, w, f, f)
            notch_can   = notch_can * notch_now
        
        self.notchf  = notch_can
        

        
    
if __name__ == '__main__': 
    
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
    
    myctparam = ControlParam()
    xparam  = myctparam.xinitial(4)
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

