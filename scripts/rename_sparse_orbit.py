# top k orbits with worst quality

import os
import pandas as pd 
from constant import *
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from loguru import logger
import glob



total = len(glob.glob(os.path.join(DIR, r"LOLARDR_*.*O")))
for file_ in tqdm(glob.iglob(os.path.join(DIR, r"LOLARDR_*.*O")), total=total):
	data = pd.read_csv(file_, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
	t_s = data["t1"].iloc[0] + data["t2"].iloc[0] / 28
	t_e = data["t1"].iloc[-1] + data["t2"].iloc[-1] / 28
	t_r = len(data)
	t_c = (t_e - t_s) * 28
	if t_r / t_c < 0.95:
		out = file_[:-1] + "D"
		logger.info(f"rename file: {file_}")
		try:
			os.rename(file_, out)
		except:
			logger.warning(f"file not exist: {file_}")

