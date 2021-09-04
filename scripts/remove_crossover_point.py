## 去除异常的交叉点

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from loguru import logger


cp_fp = f"crossover{TYPE}.txt" # 交叉点文件信息


# 读取到pandas中
df = pd.read_csv(os.path.join(DIR, cp_fp), names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")



h = df['dalt']
q1 = h.quantile(0.25)
q3 = h.quantile(0.75)
iqr = q3 - q1 
up = q3 + 1.5*iqr
down = q1 - 1.5*iqr
df1 = df.loc[h[h<up][h>down].index]
# TODO: log some info
logger.info(f"remove {TYPE} cp: {len(df)-len(df1)}")
df1.to_csv(os.path.join(DIR, cp_fp), sep=" ", header = 0, index=0, float_format="%.7f")