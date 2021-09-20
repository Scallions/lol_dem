""" 
从区域里面提取文件
"""
import glob
from re import T
import pandas as pd
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import os
import tool
from loguru import logger

dirs = [
	"data/297.000000,339.300000,-87.000000,-85.000000",
	"data/297.000000,339.300000,-85.000000,-83.000000"
]

region = [334.1, 339.3, -87, -85.73]
out_dir = ",".join([f"{r:.4f}" for r in region])
out_dir = "data/" + out_dir + "/"

logger.info(f"outdir: {out_dir}")
if not os.path.exists(out_dir):
	os.mkdir(out_dir)

tracks_dic = {}

def merge_track(track1, track2):
	track = pd.concat([track1, track2])
	track["t"] = track["t1"] + track["t2"]/28
	track = track.sort_values("t", ascending=True)
	return track.iloc[:,:-1]

def extract_track(track_name):
	track = tracks_dic[track_name]
	track = track[track["lon"]>region[0]]
	track = track[track["lon"]<region[1]]
	track = track[track["lat"]>region[2]]
	track = track[track["lat"]<region[3]]
	if len(track) != 0:
		track.to_csv(out_dir+track_name, sep=" ", header = 0, index=0, float_format="%.7f")

# 遍历目录
for dir in dirs:
	dir_ = dir+"/*.*R"
	total = len(glob.glob(dir_))
	for file_ in tqdm(glob.iglob(dir_), total=total):
		track_name = file_.split("/")[-1]
		try:
			track = tool.read_data(file_)
		except:
			continue
		if track_name in tracks_dic:
			# 融合轨道
			tracks_dic[track_name] = merge_track(track, tracks_dic[track_name])
		else:
			tracks_dic[track_name] = track


# 提取数据
process_map(extract_track, list(tracks_dic.keys()), max_workers=48, chunksize=48)



