from constant import REGION
import pandas as pd 
import glob
from pathlib import Path
import os 
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
# import pygmt
from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging
from pykrige.rk import RegressionKriging
import random

import tool
from constant import *


## read data
aorbits = []
dorbits = []
datas = None
if FUSE:
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AFC")):
        data =  tool.read_data(file_)[['lon','lat','alt']]
        if datas is None:
            datas = data
        else:
            datas = pd.concat([datas, data],ignore_index=True)
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DFC")):
        data =  tool.read_data(file_)[['lon','lat','alt']]
        datas = pd.concat([datas, data],ignore_index=True) 
else:
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AO")):
        data =  tool.read_data(file_)[['lon','lat','alt']]
        if datas is None:
            datas = data
        else:
            datas = pd.concat([datas, data],ignore_index=True)
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DO")):
        data =  tool.read_data(file_)[['lon','lat','alt']]
        datas = pd.concat([datas, data],ignore_index=True)
data = datas

# TODO: 0.25°一格
lons_n = REGION[1] - REGION[0]
lats_n = REGION[3] - REGION[2]
lons_n = int(lons_n // 0.008)
lats_n = int(lats_n // 0.008)
## imputation
n = len(data)
n_s = lons_n * lats_n
n_s = 10000
logger.info(f"data count: {n}, lons_n: {lons_n}, lats_n: {lats_n}")
# TODO: 采样调整
sample_rate = 2
if n > sample_rate * n_s:
    idxs = random.sample(range(n), sample_rate*n_s)
    lons = data["lon"].values[idxs]
    lats = data["lat"].values[idxs]
    alts = data["alt"].values[idxs]
else:
    lons = data["lon"].values
    lats = data["lat"].values
    alts = data["alt"].values
grid_lon = np.linspace(min(lons),max(lons),lons_n)
grid_lat = np.linspace(min(lats),max(lats),lats_n)
# OK = OrdinaryKriging(lons, lats, alts, variogram_model='hole-effect',coordinates_type="geographic")
OK = OrdinaryKriging(lons, lats, alts,coordinates_type="geographic")
# OK = UniversalKriging(lons, lats, alts)
# OK = RegressionKriging(lons, lats, alts,)
# OK = OrdinaryKriging(lons, lats, alts, variogram_model='hole-effect',nlags=6)
z1, ss1 = OK.execute('grid', grid_lon, grid_lat)
# #转换成网格
xgrid, ygrid = np.meshgrid(grid_lon, grid_lat)
# #将插值网格数据整理
df_grid =pd.DataFrame(dict(lon=xgrid.flatten(),lat=ygrid.flatten()))
# #添加插值结果
df_grid["alt"] = z1.flatten()
grid = xr.DataArray(z1*1000, coords=(grid_lat,grid_lon))


import pygmt
## plot dem
fig = pygmt.Figure()
fig.basemap(region=REGION, projection=f"L{(REGION[0]+REGION[1])/2}/{(REGION[2]+REGION[3])/2}/{REGION[2]}/{REGION[3]}/5i", frame=True)
pygmt.makecpt(cmap="geo", series=[alts.min(), alts.max()])
fig.grdimage(
    grid = grid,
    cmap = "geo"
)
fig.colorbar(frame=["a1000", "x+lElevation", "y+lm"])
fig.show()
fig.savefig(f"figs/{NAME}/dem_O.png")  