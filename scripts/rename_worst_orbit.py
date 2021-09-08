# top k orbits with worst quality

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from loguru import logger


cp_fp = "crossoverC.txt" # 交叉点文件信息


# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")


# # 按轨道进行统计
acps = df[["aorbit", "dalt"]].groupby("aorbit").mean().sort_values(by="dalt", ascending=False)
dcps = df[["dorbit", "dalt"]].groupby("dorbit").mean().sort_values(by="dalt", ascending=False)

# rename orbits
## ascend
# TODO: use iqr to remove 
q1 = acps.quantile(0.25).item()
q3 = acps.quantile(0.75).item()
iqr = q3 - q1
up = q3 + 1.5*iqr 
down = q1 - 1.5*iqr
for i in tqdm(acps.index):
	if acps['dalt'].at[i] < up and acps['dalt'].at[i] > down:
		continue
	out = i[:-1] + "D"
	logger.info(f"rename file: {i}")
	try:
		os.rename(i, out)
	except:
		logger.warning(f"file not exist: {i}")


## dscend
q1 = dcps.quantile(0.25).item()
q3 = dcps.quantile(0.75).item()
iqr = q3 - q1
up = q3 + 1.5*iqr 
down = q1 - 1.5*iqr
for i in tqdm(dcps.index):
	if dcps['dalt'].at[i] < up and dcps['dalt'].at[i] > down:
		continue
	out = i[:-1] + "D"
	logger.info(f"rename file: {i}")
	try:
		os.rename(i, out)
	except:
		logger.warning(f"file not exist: {i}")


## 交叉点数量
# acps = df[["aorbit", "dalt"]].groupby("aorbit").count().sort_values(by="dalt", ascending=True)
# dcps = df[["dorbit", "dalt"]].groupby("dorbit").count().sort_values(by="dalt", ascending=True)
# print(acps.head())
# print(dcps.head())

# # gate = acps.quantile(0.1).item()
# gate = 20
# for i in tqdm(acps.index):
# 	if acps['dalt'].at[i] > gate:
# 		continue
# 	out = i[:-1] + "D"
# 	logger.info(f"rename file: {i}, count: {acps['dalt'].at[i]}")
# 	try:
# 		os.rename(i, out)
# 	except:
# 		logger.warning(f"file not exist: {i}")
# # gate = dcps.quantile(0.2).item()
# for i in tqdm(dcps.index):
# 	if dcps['dalt'].at[i] > gate:
# 		continue
# 	out = i[:-1] + "D"
# 	logger.info(f"rename file: {i}, count: {dcps['dalt'].at[i]}")
# 	try:
# 		os.rename(i, out)
# 	except:
# 		logger.warning(f"file not exist: {i}")