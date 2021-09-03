"""
绘制一条轨道和dem的比较
"""
import pandas as pd 
import pygmt
import numpy as np
import glob
from pathlib import Path
import os

import tool
from constant import *


import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import xarray as xr
import tqdm


cp_fp = "crossoverO.txt" # 交叉点文件信息

# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")

# 按轨道进行统计
acps = df[["aorbit", "dalt"]].groupby("aorbit").std().sort_values(by="dalt", ascending=False)
acps = df[["aorbit", "dalt"]].groupby("aorbit").std().sort_values(by="dalt", ascending=False)
#dcps = df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=False)
#dcps = df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=False)

# 获取质量最差的轨道名
worst_afile = acps.index[0]

# 获取交叉点信息
cps = df[df["aorbit"] == worst_afile].sort_values(by="atime")
logger.info(f"worst ascend orbit: {worst_afile}, MEAN: {cps.iloc[:,8].std()}")

# 获取原始轨道
orbit = tool.read_data(worst_afile)
orbit["time"] = orbit["t1"] + orbit["t2"]/28

# 获取真实交叉点高度
aidx = cps["aidx"]
cps["alt"] = orbit.iloc[aidx, 2].values - cps["dalt"].values

# 获取dem信息
dem = xr.load_dataarray(f"data/{NAME}.nc")
dems = []
## 遍历行插值出轨道上的dem
for _, row in tqdm.tqdm(orbit.iterrows()):
	dems.append(dem.interp(lon=row["lon"], lat=row["lat"]).item()/1000)

plt.scatter(orbit["time"], dems, label="dem", s=0.5)
plt.scatter(orbit["time"], orbit["alt"], label="raw", s=0.5)
plt.scatter(cps["atime"], cps["alt"], label="cp", s=0.5)
plt.legend()
plt.savefig(f"figs/{NAME}_one_orbit_dem.png")