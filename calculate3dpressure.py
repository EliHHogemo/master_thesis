import numpy as np

def calculate3dpressure(p0,ps,hyam,hybm):
#----------------------
#   
    nlev = hyam.shape[0]
    nlat, nlon = ps.shape
#
    pressure = np.zeros( ( nlev  , nlat, nlon ) )

    for ilev in range(nlev) :

        pressure[ilev,:,:] = hyam[ilev] * p0 + hybm[ilev] * ps[:,:] # mid-level pressure
#
    return pressure
