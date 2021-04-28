# file to plot crossover and some other info, such as hist

import pandas as pd 
import numpy as np 
import glob 
from pathlib import Path
import os 
import matplotlib.pyplot as plt 

import tool

DIR = Path("./data/test/out/")
FUSE = False


aorbits = []
dorbits = []

if not FUSE:
    for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*_a.txt")): # 匹配数据文件
        data = tool.read_data(file_).to_numpy()
        aorbits.append((data, file_))

    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*_d.txt")):
        data = tool.read_data(file_).to_numpy()
        dorbits.append((data, file_))
else:
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*_a_filter.csv")):
        data = pd.read_csv(file_)[['lon','lat','alt']].to_numpy()
        aorbits.append((data, file_))
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*_d_filter.csv")):
        data = pd.read_csv(file_)[['lon','lat','alt']].to_numpy()
        dorbits.append((data, file_))

print(f"ascend orbits: {len(aorbits)}, dscend orbits: {len(dorbits)}")

dhs = []

la = len(aorbits)
ld = len(dorbits)

# plot orbit
for aorbit, file_ in aorbits:
    axs = [p[0] for p in aorbit]
    ays = [p[1] for p in aorbit]
    # axs = aorbit["lon"]
    # ays = aorbit["lat"]
    plt.plot(axs, ays, color='r', label="A")
for dorbit, file_ in dorbits:
    dxs = [p[0] for p in dorbit]
    dys = [p[1] for p in dorbit]
    # dxs = dorbit["lon"]
    # dys = dorbit["lat"]
    plt.plot(dxs, dys, color='b', label="D")


PY = True
### find cross over point
if PY:
    count = 0
    for i, (dorbit, dfile) in enumerate(dorbits):
        for j, (aorbit, afile) in enumerate(aorbits):
            k = len(aorbit)
            l = len(dorbit)
            ar, dr = tool.find_crossover(aorbit, dorbit, 0, k-1, 0, l-1)
            if ar!= -1:
                # debug info
                # print(ar, dr, k, l, i, j, afile, dfile)
                # print(aorbit[ar][:3], aorbit[ar+1][:3], dorbit[dr][:3], dorbit[dr+1][:3])
                count += 1
                cp = tool.cross_point(aorbit[ar], aorbit[ar+1], dorbit[dr], dorbit[dr+1])
                if cp[0] == -1:
                    continue
                plt.scatter(cp[0], cp[1], color='g')
                print(cp[2],cp[3])
                dhs.append(cp[2:])
else:
    cross = pd.read_csv(os.path.join(DIR,"crossover.txt"), header=None, columns=["f1","f2","c1","c2","lon","lat","alt"])
    plt.scatter()

plt.savefig("figs/crossover.png")

            

dhs = np.array(dhs)
print(len(dhs), count)
plt.close()
plt.hist(dhs[:,0] - dhs[:,1], bins=20)
plt.savefig("figs/cs_hist.png")
print(np.abs(dhs[:,0] - dhs[:,1]).mean())
# print((dhs[:,0] - dhs[:,1]).mean())
dhs = dhs[np.abs(dhs[:,0]-dhs[:,1])<0.01,:]
print(np.abs(dhs[:,0] - dhs[:,1]).mean())
