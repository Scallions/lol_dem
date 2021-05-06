import pandas as pd 
import pygmt
import numpy as np
import glob
from pathlib import Path
import os

import tool
from constant import *


files = set()

for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.[AD]R")): 
    files.add(file_[:-5]) 


def fuse_fun(x):
    x = x.sort_values(by = 'alt')
    if len(x) > 3:
        return x[1:-1].mean()
    return x.mean()

## fuse
for file_ in files:
    data = pd.DataFrame(columns=["lon","lat","alt","t1","t2"])
    data[['t1','t2']] = data[['t1','t2']].astype(int)
    for i in range(1,6):
        if os.path.exists(f"{file_}_{i}.AR"):
            temp = tool.read_data(f"{file_}_{i}.AR")
            data = pd.concat([data, temp])
    if len(data) != 0:
        data = data.groupby(['t1','t2']).apply(fuse_fun)
        data[['t1','t2']] = data[['t1','t2']].astype("int")
        data.to_csv(file_+".AF", header=0, index=0, sep=" ", float_format="%.7f")

    data = pd.DataFrame(columns=["lon","lat","alt","t1","t2"])
    data[['t1','t2']] = data[['t1','t2']].astype(int)
    for i in range(1,6):
        if os.path.exists(f"{file_}_{i}.DR"):
            temp = tool.read_data(f"{file_}_{i}.DR")
            data = pd.concat([data, temp])
    if len(data) != 0:
        data = data.groupby(['t1','t2']).apply(fuse_fun)
        data[['t1','t2']] = data[['t1','t2']].astype("int")
        data.to_csv(file_+".DF", header=0, index=0, sep=" ", float_format="%.7f")