"""
绘制单轨粗差去除前后对比图
"""

import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

from constant import *

dmax = 0

ofile = "data/1.000000,3.000000,-86.000000,-84.000000/LOLARDR_102390726_1.AO"
rfile = ofile[:-1] + 'R'
# 读取数据
if not os.path.exists(rfile):
	raise ValueError("File not exist.")
rdf = pd.read_csv(rfile, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
odf = pd.read_csv(ofile, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])

r_idx = rdf["t1"] + rdf["t2"]/28
o_idx = odf["t1"] + odf["t2"]/28

plt.figure()
plt.title(rfile.split("/")[-1])
plt.scatter(r_idx, rdf['alt'])
plt.scatter(o_idx, odf['alt'])
plt.savefig(f"figs/{NAME}/one_outlier.png")
