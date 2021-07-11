# Plot all orbit


import pandas as pd 
import pygmt
import numpy as np
import glob
from pathlib import Path
import os

import tool
from constant import *


aorbits = []
dorbits = []

# for file_ in glob.iglob(os.path.join(DIR,r"lolardr_*_a.txt")): # 匹配数据文件
#     data = tool.read_data(file_).to_numpy()[:,:3]
#     aorbits.append(data)
# for file_ in glob.iglob(os.path.join(DIR, r"lolardr_*_d.txt")):
#     data = tool.read_data(file_).to_numpy()[:,:3]
#     dorbits.append(data)

for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AR")):
    data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
    aorbits.append(data)
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DR")):
    data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
    dorbits.append(data)

print(f"A: {len(aorbits)} D: {len(dorbits)}")

Aorbits = np.vstack(aorbits)
Dorbits = np.vstack(dorbits)
orbits = np.vstack([Aorbits,Dorbits])
datas = pd.DataFrame(orbits, columns = ["lon","lat","alt"])
fig = pygmt.Figure()
# fig.basemap(region=[48.29, 211.22, -90, -89.322229], projection="A129/-90/5i", frame=True)
# fig.basemap(region=[36.285536, 49.296789, -86.9, -85.1], projection="L42/-86/-85/-87/5i", frame=True)
# fig.basemap(region=[-90, -70, 0, 20], projection="M8i", frame=True)
fig.basemap(region=REGION, projection=f"L{(REGION[0]+REGION[1])/2}/{(REGION[2]+REGION[3])/2}/{REGION[2]}/{REGION[3]}/5i", frame=True)

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
fig.savefig(f"figs/{NAME}_morbits1.png")  

for i in range(len(aorbits)):
    # aorbits[i][:,2] = i
    aorbits[i][:,2] = 1
l = len(aorbits)
for i in range(len(dorbits)):
    # dorbits[i][:,2] = i+l
    dorbits[i][:,2] = -1
aorbits = np.vstack(aorbits)
dorbits = np.vstack(dorbits)
orbits = np.vstack([aorbits,dorbits])

datas = pd.DataFrame(orbits, columns = ["lon","lat","alt"])

fig = pygmt.Figure()
# fig.basemap(region=[48.29, 211.22, -90, -89.322229], projection="A129/-90/5i", frame=True)
# fig.basemap(region=[36.285536, 49.296789, -86.9, -85.1], projection="L42/-86/-85/-87/5i", frame=True)
fig.basemap(region=REGION, projection=f"L{(REGION[0]+REGION[1])/2}/{(REGION[2]+REGION[3])/2}/{REGION[2]}/{REGION[3]}/5i", frame=True)

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
fig.savefig(f"figs/{NAME}_morbits.png")  

## remove outfiler 
aorbits = []
dorbits = []

for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AO")):
    data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
    aorbits.append(data)
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DO")):
    data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
    dorbits.append(data)

print(f"A: {len(aorbits)} D: {len(dorbits)}")

Aorbits = np.vstack(aorbits)
Dorbits = np.vstack(dorbits)
orbits = np.vstack([Aorbits,Dorbits])
datas = pd.DataFrame(orbits, columns = ["lon","lat","alt"])
fig = pygmt.Figure()
# fig.basemap(region=[48.29, 211.22, -90, -89.322229], projection="A129/-90/5i", frame=True)
# fig.basemap(region=[36.285536, 49.296789, -86.9, -85.1], projection="L42/-86/-85/-87/5i", frame=True)
fig.basemap(region=REGION, projection=f"L{(REGION[0]+REGION[1])/2}/{(REGION[2]+REGION[3])/2}/{REGION[2]}/{REGION[3]}/5i", frame=True)
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
fig.savefig(f"figs/{NAME}_morbits2.png")  

## adj 
aorbits = []
dorbits = []

for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AC")):
    data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
    aorbits.append(data)
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DC")):
    data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
    dorbits.append(data)

print(f"A: {len(aorbits)} D: {len(dorbits)}")

Aorbits = np.vstack(aorbits)
Dorbits = np.vstack(dorbits)
orbits = np.vstack([Aorbits,Dorbits])
datas = pd.DataFrame(orbits, columns = ["lon","lat","alt"])
fig = pygmt.Figure()
# fig.basemap(region=[48.29, 211.22, -90, -89.322229], projection="A129/-90/5i", frame=True)
# fig.basemap(region=[36.285536, 49.296789, -86.9, -85.1], projection="L42/-86/-85/-87/5i", frame=True)
fig.basemap(region=REGION, projection=f"L{(REGION[0]+REGION[1])/2}/{(REGION[2]+REGION[3])/2}/{REGION[2]}/{REGION[3]}/5i", frame=True)

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
fig.savefig(f"figs/{NAME}_morbits3.png")  