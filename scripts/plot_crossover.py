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

if FUSE:
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AF")):
        data = tool.read_data(file_)[['lon','lat','alt']].to_numpy()
        aorbits.append((data, file_))
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DF")):
        data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
        dorbits.append((data, file_))
else:
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.AR")):
        data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
        aorbits.append((data, file_))
    for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.DR")):
        data =  tool.read_data(file_)[['lon','lat','alt']].to_numpy()
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


PY = False
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
                    print(aorbit[ar][:2], aorbit[ar+1][:2], dorbit[dr][:2], dorbit[dr+1][:2], afile, dfile)
                    plt.scatter(float(aorbit[ar][0]), float(aorbit[ar][1]), color='y')
                    continue
                plt.scatter(cp[0], cp[1], color='g')
                # print(cp[2],cp[3])
                dhs.append(cp[2:])
    plt.savefig("figs/crossover.png")

    plt.close()
    dhs = np.array(dhs)
    print(len(dhs), count)
    plt.hist(dhs[:,0] - dhs[:,1], bins=100)
    plt.savefig("figs/cs_hist.png")
    print(np.abs(dhs[:,0] - dhs[:,1]).mean())
    # print((dhs[:,0] - dhs[:,1]).mean())
    dhs = dhs[np.abs(dhs[:,0]-dhs[:,1])<0.008,:]
    print("MAE: ",np.abs(dhs[:,0] - dhs[:,1]).mean())  
else:
    cross = pd.read_csv(os.path.join(DIR,"crossoverO.txt"), header=None, names=["f1","f2","c1","c2","ta","td","lon","lat","alt"], sep=r"\s+")
    plt.scatter(cross["lon"], cross["lat"], color='g')
    plt.savefig("figs/crossover.png")
    plt.close()
    plt.hist(cross["alt"], bins=100)
    plt.savefig("figs/cs_hist.png")
    plt.close()
    print("MAE: ", cross["alt"].abs().mean())
    print("STD: ", cross["alt"].std())
    cross["dlt"] = cross["alt"].abs()
    print(cross.sort_values("dlt", ascending=False).head())
    cross = pd.read_csv(os.path.join(DIR,"crossoverC.txt"), header=None, names=["f1","f2","c1","c2","ta","td","lon","lat","alt"], sep=r"\s+")
    plt.hist(cross["alt"], bins=100)
    plt.savefig("figs/adj1_hist.png")
    print("MAE: ", cross["alt"].abs().mean())
    print("STD: ", cross["alt"].std())
    cross["dlt"] = cross["alt"].abs()
    print(cross.sort_values("dlt", ascending=False).head())

     
    