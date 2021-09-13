from constant import * 
import numpy as np
import glob 
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map
import os


def rename(file_):
	out = file_[:-1] + "T"
	# logger.info(f"rename file: {file_}")
	try:
		os.rename(file_, out)
	except:
		logger.warning(f"file not exist: {file_}")

missions_date = {
	"CO": ["LOLARDR_091810000", "LOLARDR_092580000"],
	"NO": ["LOLARDR_092580000", "LOLARDR_102580000"],
	"SM": ["LOLARDR_102580000", "LOLARDR_113450000"],
	"ES": ["LOLARDR_113450000", "LOLARDR_231810000"],
}


start_gate = "LOLARDR_092580000"
end_gate = "LOLARDR_113450000"
# start_gate = "LOLARDR_113550000"
# end_gate = "LOLARDR_233450000"
tracks = []
for file_ in glob.iglob(os.path.join(DIR, r"LOLARDR_*.*R")):
	ff = file_.split("/")[-1]
	ff = ff.split(".")[0]
	if ff > start_gate and ff < end_gate: ## 在范围内继续 不重命名
		continue
	try:
		tracks.append(file_)
	except:
		pass

logger.info(f"rename: {len(tracks)}")
process_map(rename, tracks, max_workers=48, chunksize=48)
