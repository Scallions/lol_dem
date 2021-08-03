from constant import *
import pandas as pd
import pygmt
import numpy as np
import tool


afiles = ["data/2,22,-86,-84/LOLARDR_183451027_3.AO", "data/2,22,-86,-84/LOLARDR_111470042_3.AO", "data/2,22,-86,-84/LOLARDR_101561255_3.AO"]
# afiles = ["data/2,22,-86,-84/LOLARDR_111470042_3.AO"]
dfiles = ["data/2,22,-86,-84/LOLARDR_152231910_3.DO"]

aorbits = []
dorbits = []

for file_ in afiles:
    data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
    aorbits.append(data)
for file_ in dfiles:
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
fig.savefig("figs/cps.png")  