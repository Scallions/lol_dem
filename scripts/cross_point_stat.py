# top k orbits with worst quality

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import tool
import numpy as np


def plot_cp(df, no, t="O"):
	idx = df["dalt"].abs().argsort().iloc[-no]
	afile = df.iloc[idx,0]
	dfile = df.iloc[idx,1]
	aidx = df.iloc[idx,2]
	didx = df.iloc[idx,3]
	atrack = tool.read_data(afile)
	dtrack = tool.read_data(dfile)
	print(df.iloc[idx, -1])
	print(afile, df.iloc[idx,2])
	print(dfile, df.iloc[idx,3])
	print(df.iloc[idx,2:])
	plt.figure()
	plt.title(f"{df.iloc[idx, -1]}")
	# plot track
	plt.scatter(atrack["t1"]+atrack["t2"]/28 - df.iloc[idx,4], atrack["alt"],s=0.5, label="a")
	plt.scatter(dtrack["t1"]+dtrack["t2"]/28 - df.iloc[idx,5], dtrack["alt"],s=0.5, label="d")
	# plot neighbor point of cp
	plt.scatter(atrack["t1"][aidx:aidx+2]+atrack["t2"][aidx:aidx+2]/28 - df.iloc[idx,4], atrack["alt"][aidx:aidx+2], label="a_n")
	plt.scatter(dtrack["t1"][didx:didx+2]+dtrack["t2"][didx:didx+2]/28 - df.iloc[idx,5], dtrack["alt"][didx:didx+2], label="d_n")
	plt.vlines(0, min(atrack["alt"].min(), dtrack["alt"].min()), max(atrack["alt"].max(), dtrack["alt"].max()),linestyles = "dashed")
	plt.legend()
	plt.savefig(f"figs/{NAME}/big_cp{no}_{t}.png")
	# plot lon lat
	plt.figure()
	plt.plot(atrack["lon"][aidx:aidx+2], atrack["lat"][aidx:aidx+2], label="a_n")
	plt.plot(dtrack["lon"][didx:didx+2], dtrack["lat"][didx:didx+2], label="d_n")
	plt.scatter(df.iloc[idx,-3],df.iloc[idx,-2])
	plt.savefig(f"figs/{NAME}/big_cp_xy{no}_{t}.png")
	# 画出改正后的图
	if t == 'O':
		afile = afile[:-1] + 'C'
		dfile = dfile[:-1] + 'C'
		atrack = tool.read_data(afile)
		dtrack = tool.read_data(dfile)
		plt.figure()
		plt.title(f"{df.iloc[idx, -1]}")
		# plot track
		plt.scatter(atrack["t1"]+atrack["t2"]/28 - df.iloc[idx,4], atrack["alt"],s=0.5, label="a")
		plt.scatter(dtrack["t1"]+dtrack["t2"]/28 - df.iloc[idx,5], dtrack["alt"],s=0.5, label="d")
		# plot neighbor point of cp
		plt.scatter(atrack["t1"][aidx:aidx+2]+atrack["t2"][aidx:aidx+2]/28 - df.iloc[idx,4], atrack["alt"][aidx:aidx+2], label="a_n")
		plt.scatter(dtrack["t1"][didx:didx+2]+dtrack["t2"][didx:didx+2]/28 - df.iloc[idx,5], dtrack["alt"][didx:didx+2], label="d_n")
		plt.vlines(0, min(atrack["alt"].min(), dtrack["alt"].min()), max(atrack["alt"].max(), dtrack["alt"].max()),linestyles = "dashed")
		plt.legend()
		plt.savefig(f"figs/{NAME}/big_cp{no}_adj_{t}.png")

cp_fp = "crossoverO.txt" # 交叉点文件信息
# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")

# 输出统计信息
print("BIAS: ", df["dalt"].mean())
print("MAE: ", df["dalt"].abs().mean())
print("STD: ", df["dalt"].std())

plot_cp(df, 1)
plot_cp(df, 2)


# 按轨道进行统计
acps = df[["aorbit", "dalt"]].groupby("aorbit").std().sort_values(by="dalt", ascending=False)
dcps = df[["dorbit", "dalt"]].groupby("dorbit").std().sort_values(by="dalt", ascending=False)
## plot hist
print(acps.head())
print(dcps.head())

plt.figure()
df["dalt"].hist(bins=200)
plt.savefig(f"figs/{NAME}/cp_hist_{TYPE}.png")


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

cp_fp = "crossoverC.txt" # 交叉点文件信息


# 读取到pandas中
df1 = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")

# 输出统计信息
print("BIAS: ", df1["dalt"].mean())
print("MAE: ", df1["dalt"].abs().mean())
print("STD: ", df1["dalt"].std())

plot_cp(df1, 1, t="C")
plot_cp(df1, 2, t="C")


# 按轨道进行统计
acps = df1[["aorbit", "dalt"]].groupby("aorbit").std().sort_values(by="dalt", ascending=False)
dcps = df1[["dorbit", "dalt"]].groupby("dorbit").std().sort_values(by="dalt", ascending=False)
## plot hist
print(acps.head())
print(dcps.head())


plt.figure()
min_ = df["dalt"].mean() - 2 * df["dalt"].std()
max_ = df["dalt"].mean() + 2* df["dalt"].std()
bins = np.linspace(min_, max_, 200)
plt.hist(df["dalt"], bins=bins, alpha=0.3, density=False, label=f"raw:{df['dalt'].std():.6f}")
plt.hist(df1["dalt"], bins=bins, alpha=0.3, density=False, label=f"adj:{df1['dalt'].std():.6f}")
plt.legend()
plt.savefig(f"figs/{NAME}/compare_hist.png")