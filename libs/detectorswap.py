import numpy as np

#updated in 11/2025 
def pilatus2robot(poni_path = None, py = None, px = None):
    ponifile = open(poni_path, "r").read()
    txt = ponifile.split('\n')[5:-2]
    poni_prms = [line.split(":") for line in txt]
    # all poni distances are in meters
    dist = float(poni_prms[0][1]) 
    poniy = float(poni_prms[1][1])
    ponix = float(poni_prms[2][1])
    #
    pilatus_pixel_size = 172*1e-6 #meters
    #
    disty = poniy - py*pilatus_pixel_size
    distx = ponix - px*pilatus_pixel_size
    #
    delta = np.rad2deg(np.arctan(abs(disty/np.sqrt(distx**2 + dist**2))))
    gamma = np.rad2deg(np.arctan(abs(distx)/dist))
    #
    #tth = np.rad2deg(np.arctan(np.sqrt((py*pilatus_pixel_size - poniy)**2 + (px*pilatus_pixel_size - ponix)**2)/dist))
    #
    #print("delta angle is = ", np.round(delta, 5))
    #print("gamma angle is  = ", np.round(gamma, 5))
    #print(r"2$\theta$ is  = ", np.round(tth, 5))
    return delta, gamma