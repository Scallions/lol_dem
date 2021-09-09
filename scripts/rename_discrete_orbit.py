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
	out = file_[:-1] + "D"
	logger.info(f"rename file: {file_}")
	try:
		os.rename(file_, out)
	except:
		logger.warning(f"file not exist: {file_}")


def process_file(file_):
	data = pd.read_csv(file_, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
	if len(data) < 50:
		rename(file_)
		return
	mv_stds = data["alt"].rolling(20, min_periods=1, center=True).std() 
	mv_std = mv_stds.mean().item()
	if mv_std > 0.1:
		rename(file_)

total = len(glob.glob(os.path.join(DIR, r"LOLARDR_*.*O")))
# pool = threadpool.ThreadPool(48)

with Pool(48) as pool:
	for i in tqdm(pool.imap(process_file, glob.iglob(os.path.join(DIR, r"LOLARDR_*.*O")), chunksize=48), total=total):
		pass
pool.close()
pool.join()
r_count = total - len(glob.glob(os.path.join(DIR, r"LOLARDR_*.*O")))
logger.info(f"remove track: {r_count}")

