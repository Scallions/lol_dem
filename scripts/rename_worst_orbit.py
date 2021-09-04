# top k orbits with worst quality

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from loguru import logger


cp_fp = "crossoverO.txt" # 交叉点文件信息


# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")


# 按轨道进行统计
acps = df[["aorbit", "dalt"]].groupby("aorbit").mean().abs().sort_values(by="dalt", ascending=False)
dcps = df[["dorbit", "dalt"]].groupby("dorbit").mean().abs().sort_values(by="dalt", ascending=False)

# rename orbits
## ascend
# TODO: use iqr to remove 
gate = acps.quantile(0.9).item()
for i in tqdm(acps.index):
	if acps['dalt'].at[i] < gate:
		continue
	out = i[:-1] + "D"
	logger.info(f"rename file: {i}")
	try:
		os.rename(i, out)
	except:
		logger.warning(f"file not exist: {i}")


## dscend
gate = dcps.quantile(0.9).item()
for i in tqdm(dcps.index):
	if dcps['dalt'].at[i] < gate:
		continue
	out = i[:-1] + "D"
	logger.info(f"rename file: {i}")
	try:
		os.rename(i, out)
	except:
		logger.warning(f"file not exist: {i}")

