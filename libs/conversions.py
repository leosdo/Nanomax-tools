import numpy as np

plank = 6.6261*10**-34 # j*s
light = 2.9979*10**8 #m/s
keV_to_j = 1.602176634*10**-16 #J

def keV_angs(xray_energy):
    xray_wave = np.round(10**10*plank*light/(xray_energy*keV_to_j),4) # angstrons
    return xray_wave

def angs_keV(xray_wave):
    xray_energy = np.round(10**10*plank*light/(xray_wave*keV_to_j),4)
    return xray_energy

def newbragg(energy1, tth1, energy2):
    tthnew = np.round(2*(np.rad2deg(np.arcsin(np.sin(np.deg2rad(tth1/2))*energy1/energy2))),4)
    return tthnew