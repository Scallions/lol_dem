"""
删除没用的子块
""" 

import glob
import os
import configparser


conf = configparser.ConfigParser()
conf.read("config.ini")


for d in glob.iglob(r"data/*,*,*,*"):
	if os.path.isdir(d):
		pass
