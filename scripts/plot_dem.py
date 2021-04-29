import pandas as pd 
import glob
from pathlib import Path
import os 
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import pygmt
from pykrige.ok import OrdinaryKriging
from pykrige.uk import UniversalKriging
from pykrige.rk import RegressionKriging

import tool

DIR = Path("./data/test/out/")

## read data
aorbits = []
dorbits = []
datas = None
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AC")):
    data =  tool.read_data(file_)[['lon','lat','alt']]
    if datas is None:
        datas = data
    else:
        datas = pd.concat([datas, data],ignore_index=True)
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DC")):
    data =  tool.read_data(file_)[['lon','lat','alt']]
    datas = pd.concat([datas, data],ignore_index=True)
data = datas

## imputation
lons = data["lon"].values[::10]
lats = data["lat"].values[::10]
alts = data["alt"].values[::10]
grid_lon = np.linspace(min(lons),max(lons),200)
grid_lat = np.linspace(min(lats),max(lats),200)
OK = OrdinaryKriging(lons, lats, alts, variogram_model='hole-effect',coordinates_type="geographic")
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


## plot dem
fig = pygmt.Figure()
fig.basemap(region=[36.285536, 49.296789, -86.9, -85.1], projection="L42/-86/-85/-87/5i", frame=True)
fig.grdimage(
    grid = grid,
    cmap = "geo"
)
fig.colorbar(frame=["a1000", "x+lElevation", "y+lm"])
fig.show()
fig.savefig("figs/dem.png")  