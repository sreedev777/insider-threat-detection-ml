import pandas as pd
import os

def build_features(data_dir="data/processed"):
    """
    Builds a user-level feature table using the cleaned and labeled datasets.
    """
    # 1. Load data
    logon_df = pd.read_csv(os.path.join(data_dir, "logon_processed.csv"), parse_dates=["date"])
    file_df = pd.read_csv(os.path.join(data_dir, "file_activity_processed.csv"), parse_dates=["date"])
    device_df = pd.read_csv(os.path.join(data_dir, "device_processed.csv"), parse_dates=["date"])
    
    # 2. Extract Login Features
    # Filter only 'Logon' events for these metrics
    logons_only = logon_df[logon_df["activity"] == "Logon"].copy()
    
    # Create time-based columns
    logons_only["is_after_hours"] = (logons_only["date"].dt.hour < 6) | (logons_only["date"].dt.hour > 20)
    logons_only["is_weekend"] = logons_only["date"].dt.dayofweek >= 5
    
    login_features = logons_only.groupby("user").agg(
        login_count=("id", "count"),
        after_hours_login=("is_after_hours", "sum"),
        weekend_login=("is_weekend", "sum"),
        distinct_computers=("pc", "nunique"),
        label_logon=("label", "max") # Keep track of label for this user
    ).reset_index()
    
    # 3. Extract File Features
    # In CERT dataset, file.csv typically represents files copied to removable media.
    file_features = file_df.groupby("user").agg(
        files_accessed=("filename", "nunique"), 
        file_copy_count=("id", "count"),
        label_file=("label", "max")
    ).reset_index()
    
    # 4. Extract Device Features
    # Filter for 'Connect' events
    connects_only = device_df[device_df["activity"] == "Connect"]
    device_features = connects_only.groupby("user").agg(
        usb_connections=("id", "count"),
        label_device=("label", "max")
    ).reset_index()
    
    # 5. Merge all features by user
    # Start with a master list of all unique users across all dataframes
    all_users = pd.DataFrame({
        "user": pd.concat([logon_df["user"], file_df["user"], device_df["user"]]).unique()
    })
    
    feature_table = all_users.merge(login_features, on="user", how="left")
    feature_table = feature_table.merge(file_features, on="user", how="left")
    feature_table = feature_table.merge(device_features, on="user", how="left")
    
    # 6. Resolve Label
    # A user is marked as malicious (label=1) if they had malicious activity in ANY of the datasets
    feature_table["label"] = feature_table[["label_logon", "label_file", "label_device"]].max(axis=1)
    
    # Drop the intermediate label columns
    feature_table = feature_table.drop(columns=["label_logon", "label_file", "label_device"])
    
    # 7. Fill missing values with 0
    feature_table = feature_table.fillna(0)
    
    # Ensure count columns are integers
    for col in feature_table.columns:
        if col != "user":
            feature_table[col] = feature_table[col].astype(int)
            
    return feature_table

if __name__ == "__main__":
    df = build_features()
    print(df.head())
