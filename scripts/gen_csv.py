"""
	生成csv
"""

from constant import REGION
import pandas as pd 
import glob
from pathlib import Path
import os 
import numpy as np

import tool
from constant import *


## read data
aorbits = []
dorbits = []
datas = None
if TYPE == 'O':
    reg = r"LOLARDR_*.*O"
else:
    reg = r"LOLARDR_*.*C"
for file_ in glob.iglob(os.path.join(DIR, reg)):
    data =  tool.read_data(file_)[['lon','lat','alt']]
    if datas is None:
        datas = data
    else:
        datas = pd.concat([datas, data],ignore_index=True)
data = datas
logger.info(f"data size: {len(data)}")

data.to_csv(f"data/{NAME}.csv", index=None)