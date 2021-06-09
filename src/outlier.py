# remove outlier in single orbit file
# outlier point may lon lat or alt not only the alt

import numpy as np
from sklearn.cluster import *
from sklearn.ensemble import IsolationForest
from tqdm import tqdm

from constant import *

def proc_df(df):
    df = df[["lon","lat","alt","t1","t2"]].copy()
    a_len = 3
    d_len = 3
    dh1_kernel = np.hstack((-np.ones(d_len)/d_len,1,np.zeros(d_len)))
    dh2_kernel = np.hstack((np.zeros(d_len),1,-np.ones(d_len)/d_len))
    alts = df["alt"].to_numpy()
    dh1 = np.convolve(dh1_kernel, alts, mode="same")
    dh2 = np.convolve(dh2_kernel, alts, mode="same")
    df["dh1"] = dh1
    df["dh2"] = dh2
    return df

def kmeans_filter(datas):
    bar = tqdm(range(len(datas)))
    for j in bar:
        bar.set_description(f"Removing outlier!")
        data = datas[j]
        for i in range(ITER):
            try:
                res = KMeans(n_clusters=2).fit(data[["dh1","dh2"]].abs()) 
            except TypeError:
                print(data.shape)
            one_len = (res.labels_ == 1).sum()
            zero_len = (res.labels_ == 0).sum()
            if one_len > zero_len:
                data = data[res.labels_ == 1]
            else:
                data = data[res.labels_ == 0]
            # print(i, len(data))
            data = proc_df(data)
        datas[j] = data
    return datas