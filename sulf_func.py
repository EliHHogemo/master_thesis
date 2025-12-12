import numpy as np
import xarray as xr
import pandas as pd
import cftime
import calendar
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.path as mpath
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.ticker as mticker
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
import imageio
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime #import datetime
from glob import glob
from scipy import signal


def sulfur_burden(ds, p_lev=None, p_lev_u=None, 
                  p_lev_l=None, lat_slice=None, 
                  weighted_lat=None):
    da = ds["mmr_SULFATE"]

    Ms = 32.065
    Matmos = 5.3 * 10**21
    M_strat_air = 0.099 * Matmos   #9.9% of the total mass of the atmosphere
    Mo = 15.999
    Mso4 = Ms + (4 * Mo)
    c = Ms/Mso4

    if p_lev is not None:
        da = da.sel(lev = p_lev, method="nearest")
    elif p_lev_l is not None and p_lev_u is not None:
        da = da.where((da["lev"] >= p_lev_l) & (da["lev"] <= p_lev_u))
    elif p_lev_u is not None:
        da = da.where(da["lev"] < p_lev_u)

    if lat_slice:
        a_glob = 510000000
        h_trop = 4440
        d = 12756

        a_trop = np.pi * d * h_trop
        ratio = a_trop/a_glob
        da = da.sel(lat=slice(*lat_slice))

        da = da * M_strat_air * ratio *10**(-12)
        da = da * c
    else:
        da = da * M_strat_air *10**(-12)
        da = da * c

    
    da = da.weighted(weighted_lat).mean(dim=["lat", "lon", "lev"])

    
    return da