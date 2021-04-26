import pandas as pd 
import numpy as np 
import glob 
from pathlib import Path
import os 
import matplotlib.pyplot as plt 

import tool

DIR = Path("./data/test/out/")



aorbits = []
dorbits = []

# for file_ in glob.iglob(os.path.join(DIR,r"lolardr_*_a.txt")): # 匹配数据文件
#     data = tool.read_data(file_).to_numpy()
#     aorbits.append((data, file_))

# for file_ in glob.iglob(os.path.join(DIR, r"lolardr_*_d.txt")):
#     data = tool.read_data(file_).to_numpy()
#     dorbits.append((data, file_))

for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*_a.csv")):
    data = pd.read_csv(file_)[['lon','lat','alt']].to_numpy()
    aorbits.append((data, file_))
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*_d.csv")):
    data = pd.read_csv(file_)[['lon','lat','alt']].to_numpy()
    dorbits.append((data, file_))

print(f"ascend orbits: {len(aorbits)}, dscend orbits: {len(dorbits)}")

dhs = []

### find cross over point
for i, (dorbit, dfile) in enumerate(dorbits):
    for j, (aorbit, afile) in enumerate(aorbits):
        k = len(aorbit)
        l = len(dorbit)
        ar, dr = tool.find_crossover(aorbit, dorbit, 0, k-1, 0, l-1)
        if ar!= -1:
            # debug info
            # print(ar, dr, k, l, i, j, afile, dfile)
            # print(aorbit[ar][:3], aorbit[ar+1][:3], dorbit[dr][:3], dorbit[dr+1][:3])
            cp = tool.cross_point(aorbit[ar], aorbit[ar+1], dorbit[dr], dorbit[dr+1])
            if cp[0] == -1:
                continue
            

#             axs = [p[0] for p in aorbit]
#             ays = [p[1] for p in aorbit]
#             dxs = [p[0] for p in dorbit]
#             dys = [p[1] for p in dorbit]
#             plt.plot(axs, ays)
#             plt.plot(dxs, dys)
#             plt.scatter(cp[0], cp[1])
            # print(cp[2],cp[3])

# plt.savefig("figs/test.png")

            dhs.append(cp[2:])

dhs = np.array(dhs)
print(np.abs(dhs[:,0] - dhs[:,1]).mean())
# print((dhs[:,0] - dhs[:,1]).mean())
dhs = dhs[np.abs(dhs[:,0]-dhs[:,1])<0.01,:]
print(np.abs(dhs[:,0] - dhs[:,1]).mean())
