# read dat date. call the program
import subprocess
from constant import *

CMD = "./build/linux/x86_64/release/read_data"
DATA_DIR = "./data/dat/"

cmd = [CMD, DATA_DIR]
cmd.extend([str(r) for r in REGION])

# region = str(REGION).replace(",", " ")[1:-1]

subprocess.run(cmd)