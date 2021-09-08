"""
在地图上绘制交叉点的高程不符值，方便和dem对边观察交叉点高程不符值和高程分布有啥关系
"""

import os
import pandas as pd 
from constant import *
import pygmt
import numpy as np
import random
from loguru import logger
import tool 
import glob


# load data 
logger.info("Load data")
cp_fp = f"crossover{TYPE}.txt" # 交叉点文件信息
datas = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")
# cut_size = 1e6 # 定义抽稀阈值
# cut_ratio = 100/len(datas) # 定义抽稀率
# if len(datas) > cut_size:
#     datas = datas.iloc[random.sample(range(len(datas)), int(len(datas)*cut_ratio)),:]
datas.dalt = datas.dalt.abs()

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
datas1 = pd.DataFrame(orbits, columns = ["lon","lat","alt"])

# 绘制fig
## TODO: 把绘制地图流程抽象成函数
logger.info("Plot figure")
fig = pygmt.Figure()
fig.basemap(region=REGION, projection=f"L{(REGION[0]+REGION[1])/2}/{(REGION[2]+REGION[3])/2}/{REGION[2]}/{REGION[3]}/5i", frame=True)
pygmt.makecpt(cmap="geo", series=[datas1.alt.min()-1, datas1.alt.max()+1])
fig.plot(
    x=datas1.lon,
    y=datas1.lat,
#     sizes=0.02 * 2 ** data.magnitude,
    sizes = np.ones_like(datas1.lon)*0.02,
    color=datas1.alt,
    cmap=True,
    style="cc",
#     pen="black",
)
fig.plot(
    x=datas.lon,
    y=datas.lat,
    size = np.ones_like(datas.lon)*0.02,
    # color=datas.dalt,
	color='black',
    # cmap=True,
    style="cc",
#     pen="black",
)
fig.colorbar(frame='af+l"Elevation (km)"')
fig.savefig(f"figs/{NAME}/cp_track.png")  

logger.info("All over")