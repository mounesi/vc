

import matlab.engine
import numpy as np
import control as ct


eng = matlab.engine.start_matlab()
obj = eng.load('TFMAIN4.mat')
obj2 = obj['TF']
plant_number   = len(obj2)
tf = {}
"""
tf keys are : 
    'name'        : name of the tf
    'rd'          : response data 
    'ts'          : sampling time
    'timeunit'    : time unit usually second
    'frequency'   : frequency vector
    'frequnit'    : frequency unit
"""
for k in range(plant_number): # number of plants
    tf[k] = eng.tfreturn(k+1)

eng.quit()



#for k in range (np):

tf_frd_dict = {}
tf_frd = {}
for k in range(plant_number): # number of plants

    freq_mat = tf[k]['frequency']
    frd_len = len(freq_mat)
    freq_rad_list = []
    #freq_hz_list = []
    
    for i in range(frd_len):
        freq_rad_list.append(freq_mat[i][0])
    #    freq_hz_list.append(freq_mat[i][0]/(2*np.pi))
    
    freq_rad_array = np.array(freq_rad_list)
    
    
    rd_mat = tf[k]['rd']
    rd_list = []
    for i in range(frd_len):
        rd_list.append(rd_mat[i][0])
    
    # reconstructing rsp_fake from the data we synthesized
    # rsp is a list[np.complex] and omega is numpy.ndarray
    rsp_re_complex  = rd_list
    omega_rad_s     = freq_rad_array
    
    frd_re_omega_complex = ct.FRD(rsp_re_complex, omega_rad_s)
    #print(frd_re_omega_complex)
    
    
    tf_frd_dict[k] = frd_re_omega_complex
    tf_frd[k] = (
                {'name'     : tf[k]['name']},
                {'frdtf'    : frd_re_omega_complex},
                {'freqrad'  : freq_rad_array},
                {'rd'       : rd_list},
                {'ts'       : tf[k]['ts']},
                {'timeunit' : tf[k]['timeunit']},
                {'frequnit' : tf[k]['frequnit']}
                )

# To plot
#ct.bode_plot(frd_re_omega_complex, omega_rad_s, dB = True)

if False: 
    import pickle
    f = open("TFMAIN4.pkl","wb")
    pickle.dump(tf_frd,f)
    f.close()













    