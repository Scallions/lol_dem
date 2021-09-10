from constant import * 
import numpy as np
import glob 
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import os


def rename(file_):
	out = file_[:-1] + "T"
	# logger.info(f"rename file: {file_}")
	try:
		os.rename(file_, out)
	except:
		logger.warning(f"file not exist: {file_}")


a_gate = "LOLARDR_122600000.AO"
d_gate = "LOLARDR_122600000.DO"
total = len(glob.glob(os.path.join(DIR, r"LOLARDR_*.AO")))
tracks = []
for file_ in tqdm(glob.iglob(os.path.join(DIR, r"LOLARDR_*.AO")), total=total):
	ff = file_.split("/")[-1]
	if ff > a_gate:
		continue
	try:
		tracks.append(file_)
	except:
		pass
for file_ in tqdm(glob.iglob(os.path.join(DIR, r"LOLARDR_*.DO")), total=total):
	ff = file_.split("/")[-1]
	if ff > a_gate:
		continue
	try:
		tracks.append(file_)
	except:
		pass

process_map(rename, tracks, max_workers=48, chunksize=48)
