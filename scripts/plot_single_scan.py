import pandas as pd 
import pygmt
import numpy as np
import glob
from pathlib import Path
import os

import tool

# file_path = "./data/dat/out/lolardr_092051421_3_d.txt"
# datas = tool.read_data(file_path)
DIR = Path("./data/dat/out/")

aorbits = []
dorbits = []

for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_092060217_*_a.txt")): # 匹配数据文件
    data = tool.read_data(file_).to_numpy()[:,:3]
    aorbits.append(data)
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_092060217_*_d.txt")):
    data = tool.read_data(file_).to_numpy()[:,:3]
    dorbits.append(data)
print(f"A: {len(aorbits)} D: {len(dorbits)}")
for i in range(len(aorbits)):
    # aorbits[i][:,2] = i
    aorbits[i][:,2] = 1
l = len(aorbits)
for i in range(len(dorbits)):
    # dorbits[i][:,2] = i+l
    dorbits[i][:,2] = -1
aorbits_ = np.vstack(aorbits)
dorbits_ = np.vstack(dorbits)
orbits = np.vstack([aorbits_,dorbits_])

datas = pd.DataFrame(orbits, columns = ["lon","lat","alt"])

fig = pygmt.Figure()
fig.basemap(region=[48.29, 211.22, -90, -89.322229], projection="A129/-90/5i", frame=True)
# fig.basemap(region=[-90, -70, 0, 20], projection="M8i", frame=True)
pygmt.makecpt(cmap="geo", series=[datas.alt.min()-1, datas.alt.max()+1])
fig.plot(
    x=datas.lon,
    y=datas.lat,
#     sizes=0.02 * 2 ** data.magnitude,
    sizes = np.ones_like(datas.lon)*0.02,
    color=datas.alt,
    cmap=True,
    style="cc",
#     pen="black",
)
fig.colorbar(frame='af+l"Elevation (km)"')
fig.savefig("figs/s_scan_gmt.png")  


## matplot
import matplotlib.pyplot as plt 

for orbit in aorbits:
    plt.plot(orbit[:,0], orbit[:,1])
for orbit in dorbits:
    plt.plot(orbit[:,0], orbit[:,1])
plt.savefig("figs/s_scan_plt.png")

