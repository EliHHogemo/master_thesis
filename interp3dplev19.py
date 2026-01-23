import numpy as np

import calculate3dpressure
import interp1d

def interp3dplev19(field,ps,p0,hyam,hybm) :
#------------------------------------------
#
    '''
    MODIFICATIONS
        (2024-06-10) creation

    '''

    nlev, nlat, nlon = field.shape
#
    press19=[100000., 92500., 85000., 70000., 60000., 50000., 40000., 30000., 25000., \
             20000., 15000., 10000., 7000., 5000., 3000., 2000., 1000., 500., 100.]
    nlev19=len(press19) # number of levels

    newfield=np.zeros((nlev19,nlat,nlon), dtype=float)
#
#   
    pressure = calculate3dpressure.calculate3dpressure(ps=ps,p0=p0,hyam=hyam,hybm=hybm)
# 
    for ilat in range(0,nlat) :
        for ilon in range(0,nlon) :
            x = pressure[:,ilat,ilon]
            y = press19
            fx = field[:,ilat,ilon]

            newfield[:,ilat,ilon] = interp1d.interp1d(x=x, y=y,fx=fx)
#
    return newfield
