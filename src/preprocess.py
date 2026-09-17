import pandas as pd
import os

def clean_dataframe(df):
    """
    Converts the 'date' column to datetime and drops any rows missing 'user' or 'date'.
    """
    df_clean = df.copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])
    df_clean = df_clean.dropna(subset=['user', 'date'])
    return df_clean

def load_insider_labels(insiders_csv_path):
    """
    Loads data/answers/insiders.csv and returns a structured lookup dataframe
    containing user, start, and end dates.
    """
    insiders_df = pd.read_csv(insiders_csv_path)
    
    # Keep relevant columns and rename them
    lookup_df = insiders_df[['user', 'start', 'end']].copy()
    
    # Fix known malformed date in insiders.csv
    lookup_df['start'] = lookup_df['start'].str.replace(r'^/21/2011', '04/21/2011', regex=True)
    
    # Convert dates to datetime
    lookup_df['start'] = pd.to_datetime(lookup_df['start'], format='mixed', errors='coerce')
    lookup_df['end'] = pd.to_datetime(lookup_df['end'], format='mixed', errors='coerce')
    
    return lookup_df

def apply_labels(df, insiders_df):
    """
    Applies date-window logic to label rows as 1 if the user is malicious and 
    the event date falls within their malicious window, and 0 otherwise.
    """
    df_labeled = df.copy()
    
    # Start with all 0s
    df_labeled['label'] = 0
    
    # We can iterate through the malicious instances or merge. 
    # For simplicity and given multiple entries per user might exist, 
    # merging or applying logic per row works. Let's use an efficient method.
    
    # Group the insiders_df by user and get a list of malicious intervals just in case
    # there are multiple scenarios per user.
    for _, row in insiders_df.iterrows():
        malicious_user = row['user']
        start_date = row['start']
        end_date = row['end']
        
        # Find matching rows in df and update label
        mask = (df_labeled['user'] == malicious_user) & \
               (df_labeled['date'] >= start_date) & \
               (df_labeled['date'] <= end_date)
               
        df_labeled.loc[mask, 'label'] = 1
        
    return df_labeled

def save_processed_data(df, filename, output_dir="data/processed"):
    """
    Safely saves the DataFrame to the output_dir.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)
    print(f"Saved {filename} to {output_dir}/")
