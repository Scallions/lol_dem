""" 
去除离散的轨道
"""

import os
from threading import Thread
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from loguru import logger
import glob
# import threadpool
from multiprocessing import Pool


def rename(file_):
	out = file_ + "D"
	# logger.info(f"rename file: {file_}")
	try:
		os.rename(file_, out)
	except:
		logger.warning(f"file not exist: {file_}")


def process_file(file_):
	data = pd.read_csv(file_, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
	if len(data) < 50:
		rename(file_)
		return
	trend = data["alt"].rolling(5, min_periods=1, center=True).mean()
	delta = data["alt"] - trend
	mv_stds = delta.rolling(30, min_periods=1, center=True).std() 
	out_n = (mv_stds > 0.05).sum()
	out_p = out_n / len(mv_stds)
	if out_p > 0.05: # 越大移除越少
		rename(file_)

total = len(glob.glob(os.path.join(DIR, f"LOLARDR_*.*{TYPE}")))
# pool = threadpool.ThreadPool(48)

with Pool(48) as pool:
	for i in tqdm(pool.imap(process_file, glob.iglob(os.path.join(DIR, f"LOLARDR_*.*{TYPE}")), chunksize=48), total=total):
		pass
pool.close()
pool.join()
r_count = total - len(glob.glob(os.path.join(DIR, f"LOLARDR_*.*{TYPE}")))
logger.info(f"remove track: {r_count}")

