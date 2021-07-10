from pathlib import Path
from loguru import logger
import sys
import configparser

logger.remove()
logger.add(sys.stdout, enqueue=True)

config = configparser.ConfigParser()
config.read("./config.ini")

# 配置文件选择
key = config.defaults()["config"]

# DIR = Path("./data/202,222,-86,-84")
DIR = Path(config[key]["dir"])
NAME = config[key]["name"]
PY_ADJ = config.getboolean(key, "adj")
FUSE = config.getboolean(key, "fuse")
ITER = int(config[key]["iter"])

# region lon1 lon2 lat1 lat2 lon 0 360 lat -90 90
# REGION = [36.285536, 49.296789, -86.9, -85.1]
# REGION = [231, 246, 33, 48]
# REGION = [18, 74, -89, -85]
# REGION = [202,222,-86,-84]
REGION = config[key]["region"]
REGION = [float(r) for r in REGION.split(",")]

logger.info("load config")
logger.info(f"""
NAME: {NAME}
DIR: {DIR}
""")