# remove outlier in single orbit file
# outlier point may lon lat or alt not only the alt

import pandas as pd 
import glob
from pathlib import Path
import os 
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import *
from sklearn.ensemble import IsolationForest


ITER = 2

def read_data(file_path):
    df = pd.read_csv(file_path, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
    if df.shape[0] < 50:
        return None
    a_len = 7
    d_len = 10
    # kernel = np.ones(a_len) / a_len
    dh1_kernel = np.hstack((-np.ones(d_len)/d_len,1,np.zeros(d_len)))
    dh2_kernel = np.hstack((np.zeros(d_len),1,-np.ones(d_len)/d_len))
    # average_h = np.convolve(kernel,df["alt"].to_numpy(),mode="same")
    dh1 = np.convolve(dh1_kernel, df["alt"].to_numpy(), mode="same")
    dh2 = np.convolve(dh2_kernel, df["alt"].to_numpy(), mode="same")
    # df["alt_"] = average_h
    df["dh1"] = dh1
    df["dh2"] = dh2

    # df["dh"] = (df["alt"] - df["alt_"])
    return df

def filter(data):
    for i in range(ITER):
        res = KMeans(n_clusters=2).fit(data[["dh1","dh2"]].abs()) 
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
    return data

#### 定义txt文件目录
DIR = Path("./data/test/out/")
# datas = None
for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.AR")): # 匹配数据文件
    if os.path.exists(f"{file_[:-3]}.AO"):
        continue
    data = read_data(file_)
    data = filter(data)
    data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-3]}.AO", sep=" ", header = 0, index=0, float_format="%.7f")
    
for file_ in glob.iglob(os.path.join(DIR,r"LOLARDR_*.DR")): # 匹配数据文件
    if os.path.exists(f"{file_[:-3]}.DO"):
        continue
    data = read_data(file_)
    data = filter(data)
    data[["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-3]}.DO", sep=" ", header = 0, index=0, float_format="%.7f")
    
