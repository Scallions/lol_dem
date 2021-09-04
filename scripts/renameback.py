import os 
import glob
from constant import *

for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.*D")):
	out = file_[:-1] + "O"
	os.rename(file_, out)