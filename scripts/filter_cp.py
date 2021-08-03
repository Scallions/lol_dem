# 过滤交叉点

## 按 bias 过滤
## TODO: 对于较大从crossover.txt 中剔除
## - 大小

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt


cp_fp = "crossoverO.txt" # 交叉点文件信息


# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")
# print(df[df["dorbit"] == "data/2,22,-86,-84/LOLARDR_152231910_3.DO"]["dalt"].describe())
# print(df[df["aorbit"] == "data/2,22,-86,-84/LOLARDR_162310825_1.AO"]["dalt"].describe())

temp = df[df["dorbit"] == "data/2,22,-86,-84/LOLARDR_152231910_3.DO"].sort_values(by="dtime")
# temp = df[df["aorbit"] == "data/2,22,-86,-84/LOLARDR_112840748_5.AO"].sort_values(by="dtime")

plt.scatter(temp["dtime"], temp["dalt"])
plt.savefig("figs/orbit_cp.png")