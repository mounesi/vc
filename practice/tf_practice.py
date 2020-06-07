#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 22:55:09 2019

@author: ali
"""


import control as ct
import numpy as np


# start with a transfer function and omega vector
tf_s = ct.tf([1], [1, 2, 2])
omega_rad_s = np.logspace(-1, 2, 10)
ct.bode_plot(tf_s)
PS1 = ct.bode_plot(tf_s,omega_rad_s)
print('PS1_array of magnitude, phase, omega')
print(PS1)
print('\n')


# creating frd object from a continous transfer function
frd_omega_complex = ct.FRD(tf_s, omega_rad_s)
print('frd_omega_real_imag')
print(frd_omega_complex)
print('\n')

# interpreting absolude magnitude and phase and omega(given)
# Note that this is the same PS1
rsp_mag_phase_omega = frd_omega_complex.freqresp(omega_rad_s)
print(rsp_mag_phase_omega)
mag_abs = list(rsp_mag_phase_omega[0][0][0])
phase_rad = list(rsp_mag_phase_omega[1][0][0])
omega_res_rad_s = list(rsp_mag_phase_omega[2])
print( 'mag is :')
print (mag_abs)
print ( type(mag_abs))

print ( 'phase_rad') 
print( phase_rad)
print(type(phase_rad))
print('omega_res_rad_s')
print(omega_res_rad_s)
print(type(omega_rad_s))
# synthesizing data from the magnitude , phase and omega
rsp_re_complex = []
mag_len = len(mag_abs)

for i in range(mag_len):
    rsp_re_complex.append(mag_abs[i]*np.exp(complex(0,phase_rad[i])))
print(rsp_re_complex)
print(type(rsp_re_complex))

# reconstructing rsp_fake from the data we synthesized
# rsp is a list[np.complex] and omega is numpy.ndarray
frd_re_omega_complex = ct.FRD(rsp_re_complex, omega_rad_s)
print(frd_re_omega_complex)


# To plot
PS2 = ct.bode_plot(frd_re_omega_complex, omega_rad_s)









"""
import scipy as sp
import matplotlib.pyplot as plt
import control
import numpy as np
from simple_pid import PID
import testimport_a

control.use_matlab_defaults()
num = np.array([1])
den = np.array([1, 0, 0])
sys1 = control.tf(num, den)

a1 = control.bode_plot(sys1)

a2 = control.nyquist_plot(sys1)

control.nichols_plot(sys1)


num = np.array([1, 0])
den = np.array([1])
C = control.tf(num, den)

control.gangof4_plot(sys1, C) #  sensitivity functions [T, PS; CS, S]

# L = CP
# T = L/(1+L)   top left
# PS = P/(1+L)  top right
# CS = C/(1+L)  bottom left
# S = 1/(1+L)   bottom right
# S + T = 1


print(sys1,C)


L = sys1*C
S = control.bode_plot(1/(1 + L))


T = control.minreal(L/(1 + L))
T_res = control.bode_plot(T)
print(T)


PS = control.bode_plot(sys1/(1 + L))
CS = control.bode_plot(C/(1 + L))


t, y1 = control.impulse_response(T)

import matplotlib.pyplot as plt


plt.figure(1)
plt.plot(y1)
plt.legend('cet')
"""
