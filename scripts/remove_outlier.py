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


def read_data(file_path):
    df = pd.read_csv(file_path, header=None, sep=r"\s+", names=["lon","lat","alt","t1","t2"])
    if df.shape[0] < 50:
        return None
    a_len = 7
    d_len = 10
    kernel = np.ones(a_len) / a_len
    dh1_kernel = np.hstack((-np.ones(d_len)/d_len,1,np.zeros(d_len)))
    dh2_kernel = np.hstack((np.zeros(d_len),1,-np.ones(d_len)/d_len))
    average_h = np.convolve(kernel,df["alt"].to_numpy(),mode="same")
    dh1 = np.convolve(dh1_kernel, df["alt"].to_numpy(), mode="same")
    dh2 = np.convolve(dh2_kernel, df["alt"].to_numpy(), mode="same")
    df["alt_"] = average_h
    df["dh1"] = dh1
    df["dh2"] = dh2

    df["dh"] = (df["alt"] - df["alt_"])
    return df

def filter(data):
    res = KMeans(n_clusters=2).fit(data[["dh1","dh2"]].abs()) 
#     res = AgglomerativeClustering(n_clusters=2).fit(data[["dh1","dh2"]].abs())
    # yhat = IsolationForest(contamination=0.03).fit_predict(data[["dh1","dh2"]].abs())
#     res = OPTICS().fit(data[["dh1","dh2"]].abs())
#     data["label"] = res.labels_
    one_len = (res.labels_ == 1).sum()
    zero_len = (res.labels_ == 0).sum()
    if one_len > zero_len:
        data["label"] = (res.labels_ == 1)
    else:
        data["label"] = (res.labels_ == 0)
    return data

#### 定义txt文件目录
DIR = Path("./data/test/out/")
# datas = None
for file_ in glob.iglob(os.path.join(DIR,r"*.txt")): # 匹配数据文件
    data = read_data(file_)
    data = filter(data)
    data[data["label"] == True][["lon","lat","alt","t1","t2"]].to_csv(f"{file_[:-4]}_filter.csv")
    
