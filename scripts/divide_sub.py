"""  
将大块区域轨道划分为小块区域并添加到配置文件中去
"""

from constant import * 
import numpy as np
import glob 
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import os
import tool
import configparser

lon1, lon2, lat1, lat2 = REGION

lons = np.linspace(lon1, lon2, 5)
lats = np.linspace(lat1, lat2, 5)

# pool = Pool(48)


## 读取所有轨道文件
tracks = []
logger.info("reading tracks")
a_gate = "LOLARDR_122600000.AR"
d_gate = "LOLARDR_122600000.DR"
total = len(glob.glob(os.path.join(DIR, r"LOLARDR_*.AR")))
for file_ in tqdm(glob.iglob(os.path.join(DIR, r"LOLARDR_*.AR")), total=total):
	ff = file_.split("/")[-1]
	if ff < a_gate:
		continue
	tracks.append((file_, tool.read_data(file_)))
total = len(glob.glob(os.path.join(DIR, r"LOLARDR_*.DR")))
for file_ in tqdm(glob.iglob(os.path.join(DIR, r"LOLARDR_*.DR")), total=total):
	ff = file_.split("/")[-1]
	if ff < d_gate:
		continue
	tracks.append((file_, tool.read_data(file_)))
logger.info(f"end read tracks. Nums: {total}")

## 打开配置文件
config_f = open("data/temp_config.ini", "w+")
config = configparser.ConfigParser()
config.read("data/config.ini")
config.setdefault("config", NAME)

def append_conf(lon1, lon2, lat1, lat2, i, j):
	# config_f.write()
	global config
	config.add_section(f"{NAME}_{i}_{j}")
	config.set(f"{NAME}_{i}_{j}", "name", f"{NAME}_{i}_{j}")
	config.set(f"{NAME}_{i}_{j}", "dir", f"data/{lon1},{lon2},{lat1},{lat2}")
	config.set(f"{NAME}_{i}_{j}", "region", f"{lon1},{lon2},{lat1},{lat2}")
	if not os.path.exists(f"data/{lon1},{lon2},{lat1},{lat2}"):
		logger.info(f"make dir: data/{lon1},{lon2},{lat1},{lat2}")
		os.mkdir(f"data/{lon1},{lon2},{lat1},{lat2}")

def extract_one(args):
	global tracks
	t_i, region = args
	file_, track = tracks[t_i]
	ff = file_.split("/")[-1]
	lon1, lon2, lat1, lat2 = region
	if os.path.exists(f"data/{lon1},{lon2},{lat1},{lat2}/{ff}"):
		return
	sub_track = track[(track["lon"]>lon1) & (track["lon"]<lon2) & (track["lat"]>lat1) & (track["lat"]<lat2)]
	if len(sub_track) < 50:
		return 
	sub_track.to_csv(f"data/{lon1},{lon2},{lat1},{lat2}/{ff}", sep=" ", header = 0, index=0, float_format="%.7f")

tasks = []
for i in range(len(lons)-1):
	for j in range(len(lats)-1):
		lon1, lon2 = lons[i:i+2]
		lat1, lat2 = lats[j:j+2]
		append_conf(lon1, lon2, lat1, lat2, i, j)
		for k in range(len(tracks)):
			tasks.append((k, (lon1, lon2, lat1, lat2)))

logger.info("start divide")
process_map(extract_one, tasks, max_workers=48, chunksize=48)

config.write(config_f)
config_f.close()
os.rename("data/temp_config.ini", "config.ini")