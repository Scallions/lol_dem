# read dat date. call the program
import subprocess
import glob
import os
import pandas as pd
from loguru import logger

from constant import *

CMD = "./build/linux/x86_64/release/read_data"
DATA_DIR = "./data/dat/"


def read_raw(path):
    """
    Read data from raw binary file.
    """
    cmd = [CMD, DATA_DIR]
    cmd.extend([str(r) for r in REGION])
    subprocess.run(cmd)

def read_data(file_path, header=None):
    """
    read data in path

    Return: dataframe
    """
    return pd.read_csv(file_path, header=header, sep=r"\s+", names=["lon","lat","alt","t1","t2"],dtype = {'t1': int, 't2': int})

def load_data(data_type, data_dir = DIR):
    """
    Load data with selected type in DIR path.
    """
    aorbits = []
    dorbits = []
    logger.info(f"Load data: DIR: {os.getcwd()}/{data_dir}, type: {data_type}")
    for file_ in glob.iglob(os.path.join(data_dir, f"LOLARDR_*.A{data_type}")):
        data = read_data(file_)[['lon','lat','alt']].to_numpy()
        aorbits.append((data, file_))
    for file_ in glob.iglob(os.path.join(data_dir, f"LOLARDR_*.D{data_type}")):
        data =  read_data(file_)[['lon','lat','alt']].to_numpy()
        dorbits.append((data, file_))
    return (aorbits, dorbits)

def save_data(data, data_type, data_dir = DIR):
    """
    save data to dir with type info
    """
    for orbit_name, orbit in data:
        orbit.to_csv(f"{orbit_name}.{data_type}")


def read_crossover_points():
    """
    read crossover point infos in the crossover programe out file
    """
    cross_fp = "test"
    
    return 1