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
maxfile = ""
for ofile in tqdm(glob.iglob(os.path.join(DIR,r"LOLARDR_*.*O")), total=len(glob.glob(os.path.join(DIR, r"LOLARDR_*.*O")))):
	rfile = ofile[:-1] + 'R'
	# 读取数据
	if not os.path.exists(rfile):
		raise ValueError("File not exist.")
	rdf = pd.read_csv(rfile, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
	odf = pd.read_csv(ofile, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
	if dmax > len(rdf) - len(odf):
		continue 
	dmax = max(dmax, len(rdf) - len(odf))
	r_idx = rdf["t1"] + rdf["t2"]/28
	o_idx = odf["t1"] + odf["t2"]/28
	maxfile = rfile
	
	plt.figure()
	plt.title(rfile.split("/")[-1])
	plt.scatter(r_idx, rdf['alt'])
	plt.scatter(o_idx, odf['alt'])
	plt.savefig(f"figs/{NAME}/outlier.png")

print(maxfile)