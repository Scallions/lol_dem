from pathlib import Path
from loguru import logger
import sys
import configparser

logger.remove()
logger.add(sys.stdout, enqueue=True)

config = configparser.ConfigParser()
config.read("./config.ini")

# DIR = Path("./data/202,222,-86,-84")
DIR = Path(config["custom"]["dir"])
NAME = config["custom"]["name"]
PY_ADJ = config.getboolean("custom", "adj")
FUSE = config.getboolean("custom", "fuse")
ITER = int(config["custom"]["iter"])

# region lon1 lon2 lat1 lat2 lon 0 360 lat -90 90
# REGION = [36.285536, 49.296789, -86.9, -85.1]
# REGION = [231, 246, 33, 48]
# REGION = [18, 74, -89, -85]
# REGION = [202,222,-86,-84]
REGION = config["custom"]["region"]
REGION = [float(r) for r in REGION.split(",")]