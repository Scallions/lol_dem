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

# for file_ in glob.iglob(os.path.join(DIR,r"lolardr_*_a.txt")): # 匹配数据文件
#     data = tool.read_data(file_).to_numpy()
#     aorbits.append((data, file_))

# for file_ in glob.iglob(os.path.join(DIR, r"lolardr_*_d.txt")):
#     data = tool.read_data(file_).to_numpy()
#     dorbits.append((data, file_))

for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*_a_filter.csv")):
    data = pd.read_csv(file_)[['lon','lat','alt']].to_numpy()
    aorbits.append((data, file_))
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*_d_filter.csv")):
    data = pd.read_csv(file_)[['lon','lat','alt']].to_numpy()
    dorbits.append((data, file_))

print(f"ascend orbits: {len(aorbits)}, dscend orbits: {len(dorbits)}")


la = len(aorbits)
ld = len(dorbits)

### find cross over point
cs = []
dhs = []
for i, (dorbit, dfile) in enumerate(dorbits):
    for j, (aorbit, afile) in enumerate(aorbits):
        k = len(aorbit)
        l = len(dorbit)
        ar, dr = tool.find_crossover(aorbit, dorbit, 0, k-1, 0, l-1)
        if ar!= -1:
            cp = tool.cross_point(aorbit[ar], aorbit[ar+1], dorbit[dr], dorbit[dr+1])
            if cp[0] == -1:
                continue
            cs.append([i,j,ar,dr, cp[2]-cp[3]])
            dhs.append(cp[2:])

lc = len(cs)
v = np.ones((lc*2))
# x = np.ones(((la+ld)*2, 1))
A = np.zeros((lc*2, (la+ld)*2))

for i, c in enumerate(cs):
    v[2*i] = c[-1] / 2 
    v[2*i+1] = -c[-1] /2
    A[2*i][2*c[0]] = 1
    A[2*i][2*c[0]+1] = c[2]
    A[2*i+1][2*c[1]] = 1
    A[2*i+1][2*c[1]+1] = c[3]


# x = (A^TPA)^{-1} A^T P l
# x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A)), np.transpose(A)), v)

x = lsq_linear(A, v)
x = x.x 
v = np.dot(A, x)

dhs = np.array(dhs)
print("Before adj: ", np.abs(dhs[:,0] - dhs[:,1]).mean())
print("After adj: ", np.abs(v[0::2] - v[1::2]).mean())