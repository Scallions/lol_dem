# 初始化 交叉点平差的系数

import os
import pandas as pd 
from constant import *


cp_fp = "crossoverO.txt" # 交叉点文件信息

# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")

# 按轨道进行统计
print(df[["aorbit", "dalt"]].groupby("aorbit").mean().abs().sort_values(by="dalt", ascending=True).head())
print(df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=True).head())