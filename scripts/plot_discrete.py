""" 
plot离散的轨道
"""

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from loguru import logger
import glob
# import threadpool




total = len(glob.glob(os.path.join(DIR, r"LOLARDR_*.*O")))

m_std = 0
m_file = 0

for file_ in tqdm(glob.iglob(os.path.join(DIR, r"LOLARDR_*.*O")), total=total):
	data = pd.read_csv(file_, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
	rdf = data
	r_idx = rdf["t1"] + rdf["t2"]/28
	trend = data["alt"].rolling(30, min_periods=1, center=True).mean()
	delta = data["alt"] - trend
	mv_stds = delta.rolling(30, min_periods=1, center=True).std() 
	out_n = (mv_stds > 0.1).sum()
	out_p = out_n / len(mv_stds)
	if out_p > m_std: # 越大移除越少
		m_std = out_p
		m_file = file_
		plt.figure()
		plt.title(m_std)
		plt.plot(r_idx, trend)
		plt.scatter(r_idx, rdf['alt'], s=0.5, c="red")
		plt.savefig(f"figs/{NAME}/discreate.png")


logger.info(f"m file: {m_file}")