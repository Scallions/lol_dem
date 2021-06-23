import subprocess
from constant import *

CMD = "./build/linux/x86_64/release/crossover"
# DATA_DIR = "./data/test/"

region_str = [str(r) for r in REGION]
# region_str = " ".join(region_str)

# print(CMD, DIR, region_str)

subprocess.run([CMD, DIR, *region_str])