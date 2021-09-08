"""
删除没用的子块
""" 

import glob
import os
import configparser
import shutil
from constant import *

conf = configparser.ConfigParser()
conf.read("config.ini")


for d in glob.iglob(r"data/*,*,*,*"):
	# logger.info(d)
	if not os.path.isdir(d):
		continue
	flag = False
	for sec in conf.sections():
		dd = conf.get(sec, "dir")
		if dd == d:
			flag = True
	
	if flag == False:
		# print(d)
		# os.rmdir(d)
		logger.info(f"rmove dir: {d}")
		shutil.rmtree(d)

for d in glob.iglob(r"figs/*"):
	if not os.path.isdir(d) and "other" in d:
		continue
	dd = d.split('/')[-1]
	if dd not in conf.sections():
		# os.rmdir(d)
		# print(d)
		logger.info(f"rmove dir: {d}")
		shutil.rmtree(d)
