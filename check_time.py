import numpy as np
import xarray as xr
import pandas as pd
import cftime
import calendar
import datetime #import datetime
from glob import glob
import time
import os
import json
import dask
from dask.distributed import Client, progress, LocalCluster


def extract_vars(fld=None,tapes=["h0"],vars=["TREFHT"], ystart=None, yend=None, outfld=None, ow=True,client=None):
  """ 
  Extracts variables from NorESM history tapes
  And writes them to outfld for 1 file per variable per tape.
  Arguments:
    fld    [str]         - path to NorESM component history folder
    tape   [list of str] - list with names of hist tapes (h0,h1...) def: ["h0"]
    vars   [list of str] - list of variables def: ["TREFHT"]
    ystart [int]         - year to start from def: None (All available years)
    yend   [int]         - year to end with def: None (All available years)
    outfld [str]         - path to output folder def: cwd
        output files are written as outfld/case_name_var_tape_ystart-yend.nc
    ow     [logical]     - Overwrite output flag def: True
  
  """ 
  stime = time.perf_counter()

  #check args
  if fld is None:
    print('fld is None')
    raise
  else:
    if fld[-1] == "/":
      fld=fld[:-1]
    if not os.path.isdir(fld):
      print(("{fld} does not exit"))
      raise

  glob_tapes=[None] * len(tapes)
  for i,tape in enumerate(tapes):
    glob_file = sorted(glob(f"{fld}/*{tape}*.nc"))

    if len(glob_file)<1:
      raise ValueError(f"there is no {tape} tape in {fld}")
    #fsplitd = {"pref": fsplit[0],"comp": fsplit[1],"tape": fsplit[2],"yr":int(fsplit[3][0:4])}
    fsplitd = {"path": [], "pref": [],"comp": [],"tape":[],"year":[]}
    for j,f in enumerate(glob_file):
      fsplit=f.split(".")
      #remove .nc"
      fsplit=fsplit[:-1]
      fsplitd["pref"].append(os.path.basename(fsplit[0]))
      fsplitd["comp"].append(fsplit[1])
      fsplitd["tape"].append(fsplit[2])
      fsplitd["year"].append(int(fsplit[3][0:4]))
      fsplitd["path"].append(f)
      
    avail_yrs = sorted(list(set(fsplitd["year"])))

    if ystart is None:
      ystart = min(avail_yrs)
    if yend is None:
      yend = max(avail_yrs)
    
    if yend<ystart:
      print(f"{ystart} is smaller than {yend}")
      raise

    if ystart not in avail_yrs or yend not in avail_yrs:
      print(f"{ystart} or {yend} are not within available years: {min(avail_yrs)} - {max(avail_yrs)}")
      raise

    tmp = {"path": [], "pref": [],"comp": [],"tape":[],"year":[]}

    for l,k in enumerate(fsplitd["year"]):
      if k >= ystart and k <= yend:
        for key in fsplitd.keys():
          tmp[key].append(fsplitd[key][l])
    fsplitd = tmp
    
    glob_tapes[i] = {"tape":tape,"files":glob_file,"desc":fsplitd}
    ds = xr.open_dataset(fsplitd["path"][0])
    all_vars = list(ds.data_vars.keys())
    if vars is None:
      raise ValueError("vars is None, please provide at least one variable to extract")
    for var in vars:
      if var not in all_vars: 
        raise ValueError(f"{var} is not in {tape} tape")
      outfld_var = None
      if outfld is None:
        outfld=os.getcwd()
      if outfld[-1] == "/":
        outfld=outfld[:-1]
      bname = os.path.basename(fsplitd["pref"][0].split("/")[-1])
      outfld_bname = f"{outfld}/{bname}"
      if not os.path.isdir(outfld_bname):
        mkdir_cmd = f"mkdir -p {outfld_bname}"
        print(mkdir_cmd)
        os.system(mkdir_cmd)

      outfile = f"{outfld_bname}/{var}_{tape}_{ystart}-{yend}.nc"

      if os.path.isfile(outfile) and ow==False:
        print(f"{outfile} exists and ow is False, skipping...")
      else:
        print(f"Extracting {var} from {tape} tape for years {ystart}-{yend}...")
        file_list = ""
        for p in fsplitd["path"]:
          file_list = file_list + " " + p
        cmd = f"ncrcat -O -v {var} {file_list} {outfile}"
        #print(cmd)
        os.system(cmd)

  etime = time.perf_counter()
  ptime=etime-stime
  print(f"Script execution time: {ptime:.4f} seconds")


