# top k orbits with worst quality

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt


cp_fp = "crossoverO.txt" # 交叉点文件信息


# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")


# 按轨道进行统计
acps = df[["aorbit", "dalt"]].groupby("aorbit").std().sort_values(by="dalt", ascending=False)
dcps = df[["dorbit", "dalt"]].groupby("dorbit").std().sort_values(by="dalt", ascending=False)
## plot hist
print(acps.head())
print(dcps.head())

plt.figure()
acps.hist(bins=50)
plt.savefig(f"figs/{NAME}/a_hist.png")
plt.figure()
dcps.hist(bins=50)
plt.savefig(f"figs/{NAME}/d_hist.png")


# TODO: 画出质量最差的轨道
if False:
	worst_afile = acps.index[0]
	temp = df[df["aorbit"] == worst_afile].sort_values(by="dtime")
	print(worst_afile, acps[worst_afile])
	plt.scatter(temp["dtime"], temp["dalt"])
	plt.savefig(f"figs/worst_orbit.png")
	print(temp["dalt"].mean())


# 输出质量最差的几条轨道

# TODO: 筛选最大的几个输出到文件

# cp_fp = "crossoverC.txt" # 交叉点文件信息


# # 读取到pandas中
# df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")


# # 按轨道进行统计
# print(df[["aorbit", "dalt"]].groupby("aorbit").mean().abs().sort_values(by="dalt", ascending=False).head())

# print(df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=False).head()) 

# TODO: 把最差的文件后缀改为 [A|D]W