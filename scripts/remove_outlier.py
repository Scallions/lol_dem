# remove outlier in single orbit file
# outlier point may lon lat or alt not only the alt

from typing import Type
import pandas as pd 
import glob
from pathlib import Path
import os 
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import *
from sklearn.ensemble import IsolationForest
from tqdm import tqdm

from constant import *

def proc_df(df):
    df = df[["lon","lat","alt","t1","t2"]].copy()
    a_len = 3
    d_len = 3
    # kernel = np.ones(a_len) / a_len
    dh1_kernel = np.hstack((-np.ones(d_len)/d_len,1,np.zeros(d_len)))
    dh2_kernel = np.hstack((np.zeros(d_len),1,-np.ones(d_len)/d_len))
    # average_h = np.convolve(kernel,df["alt"].to_numpy(),mode="same")
    alts = df["alt"].to_numpy()
    dh1 = np.convolve(dh1_kernel, alts, mode="same")
    dh2 = np.convolve(dh2_kernel, alts, mode="same")
    # df["alt_"] = average_h
    df["dh1"] = dh1
    df["dh2"] = dh2
    return df

def read_data(file_path):
    try:
        df = pd.read_csv(file_path, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
    except:
        print(f"error load: {file_path}")
        os.remove(file_path)
        return None
    if df.shape[0] < 50:
        return df
    for i in range(3):
        df = proc_df(df)
    return df

def filter(data):
    # kmeans
    # for i in range(ITER):
    #     try:
    #         res = KMeans(n_clusters=2).fit(data[["dh1","dh2"]].abs()) 
    #     except TypeError:
    #         print(data.shape)
    # #     res = AgglomerativeClustering(n_clusters=2).fit(data[["dh1","dh2"]].abs())
    #     # yhat = IsolationForest(contamination=0.03).fit_predict(data[["dh1","dh2"]].abs())
    # #     res = OPTICS().fit(data[["dh1","dh2"]].abs())
    # #     data["label"] = res.labels_
    #     one_len = (res.labels_ == 1).sum()
    #     zero_len = (res.labels_ == 0).sum()
    #     if one_len > zero_len:
    #         data = data[res.labels_ == 1]
    #     else:
    #         data = data[res.labels_ == 0]
    #     # print(i, len(data))
    #     data = proc_df(data)
    # return data

    ## iqr
    h = data['alt']
    q1 = h.rolling(20, min_periods=1, center=True).quantile(0.25)
    q3 = h.rolling(20, min_periods=1, center=True).quantile(0.75)
    iqr = q3 - q1 
    up = q3 + 1.5*iqr
    down = q1 - 1.5*iqr
    return data.loc[h[h<up][h>down].index]
    

#### 定义txt文件目录

l_gate = 100 # 删除少于该数量的轨道

def proc_one_track(file_):
    if os.path.exists(f"{file_[:-1]}O"):
        return
    data = read_data(file_)
    if(data is None or len(data) < l_gate):
        return
    data = filter(data)
    data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-1]}O", sep=" ", header = 0, index=0, float_format="%.7f")

print("Start filter: DIR: ", DIR, "FUSE: ", FUSE)
if FUSE:
    for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.AF")): # 匹配数据文件
        if os.path.exists(f"{file_[:-3]}.AFO"):
            continue
        data = read_data(file_)
        if(len(data) < l_gate):
            continue
        data = filter(data)
        data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-3]}.AFO", sep=" ", header = 0, index=0, float_format="%.7f")
        
    for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.DF")): # 匹配数据文件
        if os.path.exists(f"{file_[:-3]}.DFO"):
            continue
        data = read_data(file_)
        if(len(data) < l_gate):
            continue
        data = filter(data)
        data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-3]}.DFO", sep=" ", header = 0, index=0, float_format="%.7f")
else:
    total = len(glob.glob(os.path.join(DIR, r"LOLARDR_*.*R")))
    from multiprocessing import Pool
    with Pool(48) as pool:
        for i in tqdm(pool.imap(proc_one_track, glob.iglob(os.path.join(DIR, r"LOLARDR_*.*R")), chunksize=48), total=total):
            pass
    # for file_ in tqdm(glob.iglob(os.path.join(DIR,r"LOLARDR_*.*R")), total=total): # 匹配数据文件

