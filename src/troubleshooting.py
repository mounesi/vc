import pickle
plant_path = '/home/ali/p/beam/src/sys_faulty.pkl'

infile  = open(plant_path ,'rb') 
pl_faulty = pickle.load(infile) 
infile.close() 

plant_path = '/home/ali/p/beam/src/sys_healthy.pkl'

infile  = open(plant_path ,'rb') 
pl_healthy = pickle.load(infile) 
infile.close() 

import control as ct
from vibration import Plant, Const

mypl = Plant()
mypl.run(Const.PLANT_PATH)
omega_rad_s = mypl.freq


#print('using breakdown')
#ct.margin((mag_abs,phase_rad,omega_res_rad_s))
#print(ct.margin(rsp_mag_phase_omega))

print('using margin')
print(ct.margin(pl_faulty))

#ct.margin(pl_faulty) # index 0 is out of bounds for axis 0 with size 0

#from control import matlab 
#print('using matlab on python')
#print(matlab.margin(rsp_mag_phase_omega))

#ct.bode(pl_healthy, omega_rad_s, Hz=None)
# ct.bode_plot(pl_healthy, mypl.freq)
#ct.bode_plot(pl_faulty, mypl.freq)

#print(pl_healthy)
#print(pl_faulty)


"""
#rsp_mag_phase_omega = pl_healthy.freqresp
rsp_mag_phase_omega = pl_healthy.freqresp(omega_rad_s)
#print(rsp_mag_phase_omega)
mag_abs = list(rsp_mag_phase_omega[0][0][0])
phase_rad = list(rsp_mag_phase_omega[1][0][0])
omega_res_rad_s = list(rsp_mag_phase_omega[2])
obsolete
"""