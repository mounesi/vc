import control as ct
import numpy as np


def pitf(kp,ki):
    return ct.tf([kp, ki], [1, 0])

def lptf(bden):
    return ct.tf([bden], [1, bden])

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


def notchtf(d, w, f):
    notch_can   = ct.tf([1],[1])
    for i in range(len(d)):
        notch_now   = Controller.notch_one(d[i], w[i], f[i], f[i])
        notch_can  = notch_can * notch_now

    return notch_can


def s2d_tf(sys,ts,method):
    return sys.sample(ts, method)

def d2frd_tf(sys_z, freq):
    return ct.FRD(sys_z, freq)



def controlbuild(kp, ki, bden, nd_v, nw_v, nf_v):

    pi = pitf(kp, ki)
    lp = lptf(bden)
    nf = notchtf(nd_v, nw_v, nf_v)

    controller_s = pi * lp * nf

    controller_z = s2d_tf(controller_s\
                       , discrete_ts, discrete_method )

    controller_frd = d2frd_tf(controller_z\
                        , eval_freq_rad)

    return controller_frd

