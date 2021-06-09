# read dat date. call the program
import subprocess
from constant import *

CMD = "./build/linux/x86_64/release/read_data"
DATA_DIR = "./data/dat/"


def dataloader(path):
    cmd = [CMD, DATA_DIR]
    cmd.extend([str(r) for r in REGION])
    subprocess.run(cmd)