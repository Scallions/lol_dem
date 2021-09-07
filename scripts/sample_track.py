"""
将原始轨道数据进行抽样
"""

import os 
import glob
from constant import *
import random


# R -> X

files = list(glob.glob(os.path.join(DIR, r"LOLARDR_*.*O")))
files = random.sample(files, 1758)

for file_ in files:
	out = file_[:-1] + "X"
	os.rename(file_, out)