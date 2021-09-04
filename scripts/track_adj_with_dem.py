"""
使用生成的dem来进行轨道调整
"""

from constant import *
import xarray as xr 
from tqdm import tqdm
import glob 
import os
import tool
from multiprocessing import Pool
from loguru import logger
import numpy as np
from scipy.optimize import lsq_linear


## 加载dem
dem = xr.load_dataarray(f"data/{NAME}.nc")

def adj_one_track(file_fp):
	orbit = tool.read_data(file_fp)
	ts = orbit['t1'] + orbit['t2']/28
	ts = ts.to_numpy()
	ts = ts - ts[0]
	ts = np.expand_dims(ts, 1)
	ones = np.ones_like(ts)
	hs = orbit['alt'].to_numpy()
	A = np.hstack([ones, ts])
	# logger.info(f"process: {file_fp}")
	## 遍历行插值出轨道上的dem
	# for i, row in tqdm(orbit.iterrows(), position=2, leave=False):
	dems = np.zeros((len(orbit),))
	for i, row in orbit.iterrows():
		dems[i] = dem.interp(lon=row["lon"], lat=row["lat"]).item()/1000
	dalt = dems - hs 
	try:
		x = lsq_linear(A, dalt)['x']
	except:
		return
	orbit["alt"] = hs + A.dot(x)
	# new_file = file_fp[:-1] + 'C'
	orbit.to_csv(f"{file_fp[:-1]}C", sep=" ", header = 0, index=0, float_format="%.7f")
	# orbit.to_csv(new_file)
	
	
	## 使用dem 对轨道进行调整
	# dems = np.array(dems)
	# logger.info(f"end: {file_fp}")


def test(ff):
	import time 
	time.sleep(0.01)

# pool = Pool(20)
total=len(glob.glob(os.path.join(DIR, r"LOLARDR_*.*O")))
with Pool(48) as pool:
	for i in tqdm(pool.imap(adj_one_track, glob.iglob(os.path.join(DIR, r"LOLARDR_*.*O")), chunksize=48), total=total):
		pass
# for file_ in tqdm(glob.iglob(os.path.join(DIR, r"LOLARDR_*.*O")), total=total):
	# adj_one_track(file_)
	# break
	# pool.apply_async(adj_one_track, args=(file_,), callback=update)	
	# pool.close()
	# pool.join()
# pbar.close()