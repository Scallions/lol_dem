import pandas as pd 
import numpy as np 
import glob 
from pathlib import Path
import os 
import matplotlib.pyplot as plt 
from scipy.optimize import lsq_linear

import tool

DIR = Path("./data/test/out/")
PY_ADJ = False


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

la = len(aorbits)
ld = len(dorbits)
print(f"ascend orbits: {la}, dscend orbits: {ld}")

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


cross = pd.read_csv(os.path.join(DIR,"crossoverO.txt"), header=None, names=["f1","f2","c1","c2","ta","td","lon","lat","alt"], sep=r"\s+")
lc = len(cross)

# stda = cross.groupby(["f1"])["alt"].agg("std")
# stdd = cross.groupby(["f2"])["alt"].agg("std")

# s = sum(stda) + sum(stdd)


if True:
    v = np.ones((lc*2))
    A = np.zeros((lc*2, (la+ld)*2))
    P = np.eye(lc*2)

    # for i in stda.index:
    #     ai = fmap[i]
    #     P[2*ai,2*ai] = stda[i] / s
    #     P[2*ai+1,2*ai+1] = stda[i] / s
    
    # for i in stdd.index:
    #     di = fmap[i]
    #     P[2*di,2*di] = stdd[i] / s
    #     P[2*di+1,2*di+1] = stdd[i] / s

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
        P[2*i,2*i] = 1 / abs(d)
        P[2*i+1, 2*i+1] = 1 / abs(d)
        A[2*i][2*ai] = 1
        A[2*i][2*ai+1] = at
        A[2*i+1][2*di] = -1
        A[2*i+1][2*di+1] = -dt
    P = P / np.sum(P)
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


# x = (A^TPA)^{-1} A^T P l
# x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A) + np.eye((la+ld)*2)), np.transpose(A)), v)
# x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A) + P), np.transpose(A)), v)

print("Before: ", cross["alt"].abs().mean(), cross["alt"].std())
# init x
X = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A) + 2 * np.eye((la+ld)*2)), np.transpose(A)), v)
print("After adj: ", np.abs(v - np.dot(A,X)).mean(), np.std(v - np.dot(A,X)))
for i in range(1):
    L = v - np.dot(A, X)
    x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), np.dot(P,A)) + np.eye((la+ld)*2)), np.transpose(A)), np.dot(P,L))
    X = X + x 
    t = v - np.dot(A, X)
    print(f"After adj({i}): ", np.abs(t).mean(), np.std(t))

x = X
# x = lsq_linear(A, v, lsq_solver="exact")
# x = x.x 
# v = np.dot(A, X)

# dhs = np.array(dhs)
# print("Before adj: ", np.abs(dhs[:,0] - dhs[:,1]).mean())

# print("After adj: ", np.abs(v[0::2] - v[1::2]).mean(), np.std(v[0::2] - v[1::2]))

plt.hist(v, bins=100)
plt.savefig("figs/adj_hist.png")



# adj
for orbit, file_ in aorbits:
    i = fmap[file_]
    x0 = x[2*i]
    x1 = x[2*i+1]
    orbit = pd.DataFrame(orbit, columns=["lon","lat","alt","t1","t2"])
    orbit["t1"] = orbit["t1"].astype("int")
    orbit["t2"] = orbit["t2"].astype("int")
    t0 = orbit["t1"][0]
    orbit["alt"] = orbit["alt"] - x0 - (orbit["t1"] - t0) * x1
    orbit.to_csv(f"{file_[:-3]}.AC", sep=" ", header = 0, index=0, float_format="%.7f")

for orbit, file_ in dorbits:
    i = fmap[file_]
    x0 = x[2*i]
    x1 = x[2*i+1]
    orbit = pd.DataFrame(orbit, columns=["lon","lat","alt","t1","t2"])
    orbit["t1"] = orbit["t1"].astype("int")
    orbit["t2"] = orbit["t2"].astype("int")
    t0 = orbit["t1"][0]
    orbit["alt"] = orbit["alt"] - x0 - (orbit["t1"] - t0) * x1
    orbit.to_csv(f"{file_[:-3]}.DC", sep=" ", header = 0, index=0, float_format="%.7f")