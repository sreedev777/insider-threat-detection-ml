import pandas as pd
import os

def load_logon(data_dir="data"):
    return pd.read_csv(os.path.join(data_dir, "logon.csv"), parse_dates=["date"])

def load_file_activity(data_dir="data"):
    return pd.read_csv(os.path.join(data_dir, "file.csv"), parse_dates=["date"])

def load_device(data_dir="data"):
    return pd.read_csv(os.path.join(data_dir, "device.csv"), parse_dates=["date"])
