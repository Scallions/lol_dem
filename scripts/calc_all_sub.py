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
import configparser
import subprocess

def do_one(args):
	i, j = args
	subprocess.run(["bash", "test.sh", f"{NAME}_{i}_{j}", ">>", "/dev/null"])
	


lon1, lon2, lat1, lat2 = REGION
lons = np.linspace(lon1, lon2, 5)
lats = np.linspace(lat1, lat2, 5)


tasks = []
for i in range(len(lons)-1):
	for j in range(len(lats)-1):
		tasks.append((i,j))


logger.info("start divide")
process_map(do_one, tasks, max_workers=48, chunksize=48)