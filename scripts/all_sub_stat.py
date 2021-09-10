""" 
计算所有分区的结果
"""
from constant import * 
import numpy as np
import glob 
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import os
import tool
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

lon1, lon2, lat1, lat2 = REGION
lons = np.linspace(lon1, lon2, 5)
lats = np.linspace(lat1, lat2, 5)


cps = None
cps_adj = None
for i in range(len(lons)-1):
	for j in range(len(lats)-1):
		lon1, lon2 = lons[i:i+2]
		dlon = lon2 - lon1
		lat1, lat2 = lats[j:j+2]
		dlat = lat2 - lat2
		lon1 = lon1-dlon*0.1
		lon2 = lon2+dlon*0.1
		lat1 = lat1-dlat*0.1
		lat2 = lat2+dlat*0.1
		data = pd.read_csv(f"data/{lon1},{lon2},{lat1},{lat2}/crossoverO.txt", names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")
		if cps is None:
			cps = data
		else:
			cps = pd.concat([cps, data],ignore_index=True)			
		data = pd.read_csv(f"data/{lon1},{lon2},{lat1},{lat2}/crossoverC.txt", names=["aorbit", "dorbit", "aidx", "didx", "atime", "dtime", "lon", "lat", "dalt"], sep=" ")
		if cps_adj is None:
			cps_adj = data
		else:
			cps_adj = pd.concat([cps_adj, data],ignore_index=True)	

plt.figure()
min_ = cps["dalt"].mean() - 2 * cps["dalt"].std()
max_ = cps["dalt"].mean() + 2* cps["dalt"].std()
bins = np.linspace(min_, max_, 200)
plt.hist(cps["dalt"], bins=bins, alpha=0.3, density=False, label=f"raw:{cps['dalt'].std():.6f}")
plt.hist(cps_adj["dalt"], bins=bins, alpha=0.3, density=False, label=f"adj:{cps_adj['dalt'].std():.6f}")
plt.legend()
plt.savefig(f"figs/{NAME}/compare_hist_sub_all.png")
