from pathlib import Path
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, enqueue=True)

DIR = Path("./data/test/out")
PY_ADJ = False
FUSE = False
ITER = 2
# region lon1 lon2 lat1 lat2 lon 0 360 lat -90 90
# REGION = [36.285536, 49.296789, -86.9, -85.1]
# REGION = [231, 246, 33, 48]
# REGION = [18, 74, -89, -85]
REGION = [202,222,-86,-84]