import os 
import glob
from constant import *
from tqdm import tqdm 

total = len(glob.glob(os.path.join(DIR, r"LOLARDR_*.*D")))

for file_ in tqdm(glob.iglob(os.path.join(DIR, r"LOLARDR_*.*D")), total=total):
	out = file_[:-1]
	os.rename(file_, out)