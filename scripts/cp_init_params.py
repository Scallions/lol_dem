# 初始化 交叉点平差的系数

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import numpy as np


cp_fp = "crossoverO.txt" # 交叉点文件信息

# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")

# 按轨道进行统计
# print(df[["aorbit", "dalt"]].groupby("aorbit").mean().abs().sort_values(by="dalt", ascending=False).head())
aorbs = df[["aorbit", "dalt"]].groupby("aorbit").mean().abs().sort_values(by="dalt", ascending=False)
# print(df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=False).head())
dorbs = df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=False)

print(aorbs.iloc[0,:])

datas = df[df["aorbit"] == "data/48.000000,89.000000,-90.000000,-89.000000/LOLARDR_100101230_4.AO"]
xs = datas["dalt"]
ts = datas["atime"]
lens = len(xs)

A = np.ones((lens, 2))
A[:,0] = ts.to_numpy()
y = xs.to_numpy()
x = np.dot(np.linalg.inv(np.dot(A.T, A)), np.dot(A.T, y))
print(x)
y_hat = np.dot(A,x)

# plt.scatter(ts, xs)
# plt.scatter(ts, y_hat, c='red')
# plt.savefig("figs/dalts.png")