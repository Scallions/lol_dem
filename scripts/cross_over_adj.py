from numpy.linalg import LinAlgError
import pandas as pd 
import numpy as np 
import glob 
import os 
import matplotlib.pyplot as plt 
from scipy.optimize import lsq_linear
import scipy.sparse as sp 
import scipy.sparse.linalg
import time
import random
# from scipy.sparse.construct import random

import tool
from constant import *


aorbits = []
dorbits = []
fmap = {}
i = 0


## load orbit

if FUSE:
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AFO")):
        data = tool.read_data(file_).to_numpy()
        aorbits.append((data, file_))
        fmap[file_] = i
        i += 1
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DFO")):
        data = tool.read_data(file_).to_numpy()
        dorbits.append((data, file_))
        fmap[file_] = i
        i += 1
else:
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

la = len(aorbits) # 升轨数量
ld = len(dorbits)   # 降轨数量
print(f"ascend orbits: {la}, dscend orbits: {ld}")


## 加载交叉点信息
if FUSE:
    cross = pd.read_csv(os.path.join(DIR,"crossoverFO.txt"), header=None, names=["f1","f2","c1","c2","ta","td","lon","lat","alt"], sep=r"\s+")
else:
    cross = pd.read_csv(os.path.join(DIR,"crossoverO.txt"), header=None, names=["f1","f2","c1","c2","ta","td","lon","lat","alt"], sep=r"\s+")



# 初始化系数
if False:
    X = np.zeros(((la+ld)*2, ))
    for k in fmap:
        v = fmap[k]
        if v < la:
            datas = cross[cross["f1"] == k]
            ts = datas["ta"]
        else:
            datas = cross[cross["f2"] == k]
            ts = datas["td"]
        xs = datas["alt"]
        # TODO: 根据 alt 的大小来初始化，超过阈值进行初始值设置
        if xs.abs().mean() > 0.5:
            ts = ts.to_numpy()
            ts = ts - ts[0]
            lens = len(xs)
            A = np.ones((lens, 2))
            A[:,0] = ts
            y = xs.to_numpy()
            if np.isnan(y).sum() > 0 or np.isnan(ts).sum() > 0:
                logger.error(f"detect nan: {k}, dalt: {np.isnan(y).sum()}, time: {np.isnan(ts).sum()}")
            try:
                x = np.dot(np.linalg.inv(np.dot(A.T, A)), np.dot(A.T, y))
            except LinAlgError as e:
                x = np.zeros((2,1))
        else:
            x = np.zeros((2,1))
        if np.isnan(x).sum() > 0:
            x = np.zeros((2,1))
        if v >= la:
            X[2*v] = -x[1]
            X[2*v+1] = -x[0]
        else:
            X[2*v] = x[1]
            X[2*v+1] = x[0]
    # X = sp.dok_matrix(X)

# simpling
# TODO: 根据数量调整，而不是直接确定倍数,采样
n = len(cross)
if n // (la+ld) > 4:
    cross = cross.sample(int(3*(la+ld)))
lc = len(cross)

# stda = cross.groupby(["f1"])["alt"].agg("std")
# stdd = cross.groupby(["f2"])["alt"].agg("std")

# s = sum(stda) + sum(stdd)


if False:
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
        # at = aorbits[ai][0][ar][-2] - aorbits[ai][0][0][-2]
        # dt = dorbits[di-la][0][dr][-2] - dorbits[di-la][0][0][-2]
        at = cross.iloc[i,4] - aorbits[ai][0][0][-2]
        dt = cross.iloc[i,5] - dorbits[di-la][0][0][-2]
        v[2*i] = d / 2 
        v[2*i+1] = -d /2
        P[2*i,2*i] = 1 / abs(d)
        P[2*i+1, 2*i+1] = 1 / abs(d)
        A[2*i][2*ai] = 1
        A[2*i][2*ai+1] = at
        A[2*i+1][2*di] = 1
        A[2*i+1][2*di+1] = dt
    P = P / np.sum(P)
else:
    v = np.ones((lc,))
    # A = np.zeros((lc, (la+ld)*2))
    # P = np.eye(lc)
    A = sp.dok_matrix((lc, (la+ld)*2))
    # P = sp.identity(lc)
    P = np.zeros((lc,))
    for i in range(lc):
        # one
        afile = cross.iloc[i,0]
        dfile = cross.iloc[i,1]
        ar = cross.iloc[i,2]
        dr = cross.iloc[i,3]
        d = cross.iloc[i,-1]
        ai = fmap[afile]
        di = fmap[dfile]
        # at = aorbits[ai][0][ar][-2] - aorbits[ai][0][0][-2]
        # dt = dorbits[di-la][0][dr][-2] - dorbits[di-la][0][0][-2]
        at = cross.iloc[i,4] - aorbits[ai][0][0][-2]
        dt = cross.iloc[i,5] - dorbits[di-la][0][0][-2]
        v[i] = d 
        # P[i,i] = 1/(abs(d)+1e-6)
        P[i] = 1/(abs(d)+1e-6)
        A[i,2*ai] = 1
        A[i,2*ai+1] = at 
        A[i,2*di] = -1
        A[i,2*di+1] = -dt
    P = P / np.sum(P)
    P = sp.diags(P)
    # P = np.diag(P)


# x = (A^TPA)^{-1} A^T P l
# x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A) + np.eye((la+ld)*2)), np.transpose(A)), v)
# x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A) + P), np.transpose(A)), v)

print("Before: ", cross["alt"].abs().mean(), cross["alt"].std())
# init x
# TODO: 分别计算初始值
start = time.time()
rhi = 2
rhi1 = 2
# use scipy ?
# I = np.eye((la+ld)*2)
I = sp.identity((la+ld)*2)
# A = A.toarray()
# v = sp.dok_matrix(v)
Atp = A.T.dot(P)
# Att = Atp.dot(A)
Att = Atp.dot(A)
# Adt = Att + rhi*I
# Adt = np.linalg.inv(Adt)
if True:
    # X = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), A) + rhi * I), np.transpose(A)), v)
    # X = sp.linalg.inv(sp.csc_matrix(A.T * A + rhi*I)) * A.T * v
    # X = sp.linalg.spsolve(A.T*A+rhi*I, A.T*v)
    # X = np.linalg.lstsq(Att, Atp.dot(v))[0]
    # X = Adt.dot(Atp.dot(v))
    X = sp.linalg.lsmr(Att, Atp.dot(v))[0]
else:
    # X = lsq_linear(A, v)
    # X = sp.linalg.lsqr(A, v, show=True) 
    X = sp.linalg.lsmr(A, v)[0]
    # X = np.linalg.lstsq(A,v)
    # X = sp.linalg.spsolve(A, v)
res = v - A.dot(X)
print("Init: ", np.abs(res).mean(), np.std(res))

# 间接平差
# PX = sp.identity((la+ld)*2)
# Add = A.T.dot(P).dot(A) + rhi1*PX
# Apd = Att + rhi1 * np.eye((la+ld)*2)
# Apd = np.linalg.inv(Apd)
for i in range(5):
    # L = v - np.dot(A, X)
    L = v - A.dot(X)
    # x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), np.dot(P,A)) + np.eye((la+ld)*2)), np.transpose(A)), np.dot(P,L))
    # x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A), np.dot(P,A)) + rhi1 * np.eye((la+ld)*2)), np.transpose(A)), np.dot(P,L))
    # x = np.linalg.lstsq(Apd, Atp.dot(L))[0]
    # x = Apd.dot(Atp.dot(L))
    # x = sp.linalg.inv(sp.csc_matrix(A.T * P * A + rhi1 * PX)) * A.T * P * L
    # x = sp.linalg.lsmr(A, L, show=True, maxiter=10)[0]
    x = sp.linalg.lsmr(Att, Atp.dot(L))[0]
    # x = np.linalg.lstsq(A.T.dot(A), A.T.dot(L))[0]
    # x = sp.linalg.spsolve(Add, A.T.dot(L))
    # x = sp.linalg.lsqr(Att, A.T.dot(L))
    # x = sp.linalg.spsolve(A.T*P*A+rhi1*PX, A.T*L)
    # x = sp.linalg.spsolve(A.T*P*A+rhi1*PX, A.T*P*L)
    X = X + x 
    # t = v - np.dot(A, X)
    t = v - A.dot(X)
    print(f"After adj({i}): ", np.abs(t).mean(), np.std(t))

end = time.time()
print("time: ", end-start)

x = X
# x = lsq_linear(A, v, lsq_solver="exact")
# x = x.x 
# v = np.dot(A, X)

# dhs = np.array(dhs)
# print("Before adj: ", np.abs(dhs[:,0] - dhs[:,1]).mean())

# print("After adj: ", np.abs(v[0::2] - v[1::2]).mean(), np.std(v[0::2] - v[1::2]))
plt.hist(v, bins=100)
plt.savefig(f"figs/{NAME}_adj_hist.png")



# adj
if FUSE:
    for orbit, file_ in aorbits:
        i = fmap[file_]
        x0 = x[2*i]
        x1 = x[2*i+1]
        orbit = pd.DataFrame(orbit, columns=["lon","lat","alt","t1","t2"])
        orbit["t1"] = orbit["t1"].astype("int")
        orbit["t2"] = orbit["t2"].astype("int")
        t0 = orbit["t1"][0]
        orbit["alt"] = orbit["alt"] - x0 - (orbit["t1"] - t0) * x1
        orbit.to_csv(f"{file_[:-4]}.AFC", sep=" ", header = 0, index=0, float_format="%.7f")

    for orbit, file_ in dorbits:
        i = fmap[file_]
        x0 = x[2*i]
        x1 = x[2*i+1]
        orbit = pd.DataFrame(orbit, columns=["lon","lat","alt","t1","t2"])
        orbit["t1"] = orbit["t1"].astype("int")
        orbit["t2"] = orbit["t2"].astype("int")
        t0 = orbit["t1"][0]
        orbit["alt"] = orbit["alt"] - x0 - (orbit["t1"] - t0) * x1
        orbit.to_csv(f"{file_[:-4]}.DFC", sep=" ", header = 0, index=0, float_format="%.7f")
else:
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