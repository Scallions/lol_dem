import pandas as pd 
import numpy as np 
import glob 
from pathlib import Path
import os 
import matplotlib.pyplot as plt 
from scipy.optimize import lsq_linear

import tool

DIR = Path("./data/test/out/")



aorbits = []
dorbits = []


fmap = {}
i = 0
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AO")):
    data = tool.read_data(file_).to_numpy()
    aorbits.append((data, file_))
    fmap[file_] = i
    i += 1
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DO")):
    data = tool.read_data(file_).to_numpy()
    dorbits.append((data, file_))
    fmap[file_] = i
    i += 1

print(f"ascend orbits: {len(aorbits)}, dscend orbits: {len(dorbits)}")


la = len(aorbits)
ld = len(dorbits)

### find cross over point
# cs = []
# dhs = []
# for i, (dorbit, dfile) in enumerate(dorbits):
#     for j, (aorbit, afile) in enumerate(aorbits):
#         k = len(aorbit)
#         l = len(dorbit)
#         ar, dr = tool.find_crossover(aorbit, dorbit, 0, k-1, 0, l-1)
#         if ar!= -1:
#             cp = tool.cross_point(aorbit[ar], aorbit[ar+1], dorbit[dr], dorbit[dr+1])
#             if cp[0] == -1:
#                 continue
#             cs.append([i,j,ar,dr, cp[2]-cp[3]])
#             dhs.append(cp[2:])

# lc = len(cs)

cross = pd.read_csv(os.path.join(DIR,"crossover.txt"), header=None, names=["f1","f2","c1","c2","lon","lat","alt"], sep=r"\s+")
lc = len(cross)

if True:
    v = np.ones((lc*2))
    A = np.zeros((lc*2, (la+ld)*2))

    for i in range(lc):
        # split
        afile = cross.iloc[i,0]
        dfile = cross.iloc[i,1]
        ar = cross.iloc[i,2]
        dr = cross.iloc[i,3]
        d = cross.iloc[i,-1]
        ai = fmap[afile]
        di = fmap[dfile]
        at = aorbits[ai][0][ar][-2] - aorbits[ai][0][0][-2]
        dt = dorbits[di-la][0][dr][-2] - dorbits[di-la][0][0][-2]
        v[2*i] = d / 2 
        v[2*i+1] = d /2
        A[2*i][2*ai] = 1
        A[2*i][2*ai+1] = at
        A[2*i+1][2*di] = -1
        A[2*i+1][2*di+1] = -dt
else:
    v = np.ones((lc*2))
    A = np.zeros((lc*2, (la+ld)*2))
    for i in range(lc):
        # one
        afile = cross.iloc[i,0]
        dfile = cross.iloc[i,1]
        ar = cross.iloc[i,2]
        dr = cross.iloc[i,3]
        d = cross.iloc[i,-1]
        ai = fmap[afile]
        di = fmap[dfile]
        at = aorbits[ai][0][ar][-2] - aorbits[ai][0][0][-2]
        dt = dorbits[di-la][0][dr][-2] - dorbits[di-la][0][0][-2]
        v[i] = d 
        A[i,2*ai] = 1
        A[i,2*ai+1] = at 
        A[i,2*di] = -1
        A[i,2*di+1] = -dt

# for i, c in enumerate(cs):
#     v[2*i] = -c[-1] / 2 
#     v[2*i+1] = c[-1] /2
#     A[2*i][2*c[0]] = 1
#     A[2*i][2*c[0]+1] = c[2]
#     A[2*i+1][2*c[1]] = 1
#     A[2*i+1][2*c[1]+1] = c[3]


# x = (A^TPA)^{-1} A^T P l
x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A) + np.eye((la+ld)*2)), np.transpose(A)), v)

# x = lsq_linear(A, v, lsq_solver="exact")
# x = x.x 
v = np.dot(A, x)

# dhs = np.array(dhs)
# print("Before adj: ", np.abs(dhs[:,0] - dhs[:,1]).mean())
print("Before: ", cross["alt"].abs().mean(), cross["alt"].std())
# print("After adj: ", np.abs(v[0::2] - v[1::2]).mean(), np.std(v[0::2] - v[1::2]))
print("After adj: ", np.abs(v).mean(), np.std(v))
plt.hist(v, bins=100)
plt.savefig("figs/adj_hist.png")


for orbit, file_ in aorbits:
    i = fmap[file_]
    x0 = x[2*i]
    x1 = x[2*i+1]
    orbit = pd.DataFrame(orbit, columns=["lon","lat","alt","t1","t2"])
    t0 = orbit["t1"][0]
    orbit["alt"] = orbit["alt"] - x0 - (orbit["t1"] - t0) * x1
    orbit.to_csv(f"{file_[:-3]}.AC", sep=" ", header = 0, index=0)

for orbit, file_ in dorbits:
    i = fmap[file_]
    x0 = x[2*i]
    x1 = x[2*i+1]
    orbit = pd.DataFrame(orbit, columns=["lon","lat","alt","t1","t2"])
    t0 = orbit["t1"][0]
    orbit["alt"] = orbit["alt"] + x0 + (orbit["t1"] - t0) * x1
    orbit.to_csv(f"{file_[:-3]}.DC", sep=" ", header = 0, index=0)