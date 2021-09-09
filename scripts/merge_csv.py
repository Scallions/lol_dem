import pandas as pd
import glob

datas = None
name = "cabeus2"
for file_ in glob.iglob(f"data/{name}_*.csv"):
    data =  pd.read_csv(file_)
    if datas is None:
        datas = data
    else:
        datas = pd.concat([datas, data],ignore_index=True)
data = datas
# logger.info(f"data size: {len(data)}")

data.to_csv(f"data/{name}-all.csv", index=None)