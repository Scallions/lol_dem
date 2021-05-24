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
    df = pd.read_csv(file_path, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
    if df.shape[0] < 50:
        return df
    return proc_df(df)

def filter(data):
    for i in range(ITER):
        try:
            res = KMeans(n_clusters=2).fit(data[["dh1","dh2"]].abs()) 
        except TypeError:
            print(data.shape)
    #     res = AgglomerativeClustering(n_clusters=2).fit(data[["dh1","dh2"]].abs())
        # yhat = IsolationForest(contamination=0.03).fit_predict(data[["dh1","dh2"]].abs())
    #     res = OPTICS().fit(data[["dh1","dh2"]].abs())
    #     data["label"] = res.labels_
        one_len = (res.labels_ == 1).sum()
        zero_len = (res.labels_ == 0).sum()
        if one_len > zero_len:
            data = data[res.labels_ == 1]
        else:
            data = data[res.labels_ == 0]
        # print(i, len(data))
        data = proc_df(data)
    return data

#### 定义txt文件目录

if FUSE:
    for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.AF")): # 匹配数据文件
        if os.path.exists(f"{file_[:-3]}.AFO"):
            continue
        data = read_data(file_)
        if(len(data) < 50):
            continue
        data = filter(data)
        data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-3]}.AFO", sep=" ", header = 0, index=0, float_format="%.7f")
        
    for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.DF")): # 匹配数据文件
        if os.path.exists(f"{file_[:-3]}.DFO"):
            continue
        data = read_data(file_)
        if(len(data) < 50):
            continue
        data = filter(data)
        data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-3]}.DFO", sep=" ", header = 0, index=0, float_format="%.7f")
else:
    for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.AR")): # 匹配数据文件
        if os.path.exists(f"{file_[:-3]}.AO"):
            continue
        data = read_data(file_)
        if(len(data) < 50):
            continue
        data = filter(data)
        data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-3]}.AO", sep=" ", header = 0, index=0, float_format="%.7f")
        
    for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.DR")): # 匹配数据文件
        if os.path.exists(f"{file_[:-3]}.DO"):
            continue
        data = read_data(file_)
        if(len(data) < 50):
            continue
        data = filter(data)
        data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-3]}.DO", sep=" ", header = 0, index=0, float_format="%.7f")
    
