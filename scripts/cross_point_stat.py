# top k orbits with worst quality

import os
import pandas as pd 
from constant import *


cp_fp = "crossoverO.txt" # 交叉点文件信息


# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")


# 按轨道进行统计
print(df[["aorbit", "dalt"]].groupby("aorbit").mean().abs().sort_values(by="dalt", ascending=False).head())

print(df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=False).head())
# 输出质量最差的几条轨道

# TODO: 筛选最大的几个输出到文件

cp_fp = "crossoverC.txt" # 交叉点文件信息


# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")


# 按轨道进行统计
print(df[["aorbit", "dalt"]].groupby("aorbit").mean().abs().sort_values(by="dalt", ascending=False).head())

print(df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=False).head()) 