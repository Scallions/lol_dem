import pandas as pd 
import pygmt
import numpy as np
import tool

file_path = "./data/dat/out/lolardr_092051421_3_d.txt"
datas = tool.read_data(file_path)
fig = pygmt.Figure()
fig.basemap(region=[48.29, 211.22, -90, -89.322229], projection="A129/-90/5i", frame=True)
# fig.basemap(region=[-90, -70, 0, 20], projection="M8i", frame=True)
pygmt.makecpt(cmap="geo", series=[datas.alt.min(), datas.alt.max()])
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
fig.savefig("figs/out.png")  