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


# load data 
logger.info("Load data")
cp_fp = "crossoverO.txt" # 交叉点文件信息
datas = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")
cut_size = 1e6 # 定义抽稀阈值
cut_ratio = 100000/len(datas) # 定义抽稀率
if len(datas) > cut_size:
    datas = datas.iloc[random.sample(range(len(datas)), int(len(datas)*cut_ratio)),:]
datas.dalt = datas.dalt.abs()


# 绘制fig
## TODO: 把绘制地图流程抽象成函数
logger.info("Plot figure")
fig = pygmt.Figure()
fig.basemap(region=REGION, projection=f"L{(REGION[0]+REGION[1])/2}/{(REGION[2]+REGION[3])/2}/{REGION[2]}/{REGION[3]}/5i", frame=True)
pygmt.makecpt(cmap="geo", series=[datas.dalt.min()-1, datas.dalt.max()+1])
fig.plot(
    x=datas.lon,
    y=datas.lat,
    size = np.ones_like(datas.lon)*0.02,
    color=datas.dalt,
    cmap=True,
    style="cc",
#     pen="black",
)
fig.colorbar(frame='af+l"Elevation (km)"')
fig.savefig("figs/all_cps.png")  

logger.info("All over")