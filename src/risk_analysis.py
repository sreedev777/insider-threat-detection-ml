import pandas as pd
import numpy as np
import joblib
import os

def main():
    print("Starting risk analysis...")
    
    data_path = 'data/processed/feature_table.csv'
    model_path = 'models/random_forest_model.pkl'
    output_path = 'reports/risk_report.csv'

    # Load data
    df = pd.read_csv(data_path)
    
    # Load model
    model = joblib.load(model_path)
    
    # Generate model_prediction
    # Exclude 'user' and 'label' columns for prediction if they exist
    features_to_drop = ['user', 'label']
    features_to_predict = [col for col in df.columns if col not in features_to_drop]
    X = df[features_to_predict]
    
    df['model_prediction'] = model.predict(X)
    
    # Calculate risk_score
    df['risk_score'] = 0
    df.loc[df['after_hours_login'] > 0, 'risk_score'] += 1
    df.loc[df['file_copy_count'] > 100, 'risk_score'] += 1
    df.loc[df['usb_connections'] > 0, 'risk_score'] += 1
    df.loc[df['model_prediction'] == 1, 'risk_score'] += 2
    
    # Calculate risk_level
    def get_risk_level(score):
        if score >= 4:
            return 'High'
        elif score >= 2:
            return 'Medium'
        else:
            return 'Low'
            
    df['risk_level'] = df['risk_score'].apply(get_risk_level)
    
    # Calculate unusual_access
    if 'department' in df.columns:
        # Calculate department stats
        dept_stats = df.groupby('department')['files_accessed'].agg(['mean', 'std']).reset_index()
        df = df.merge(dept_stats, on='department', how='left')
        
        # If std is NaN (e.g. only 1 user in dept), fill with 0
        df['std'] = df['std'].fillna(0)
        
        df['unusual_access'] = df['files_accessed'] > (df['mean'] + 2 * df['std'])
        
        # Drop temporary columns
        df = df.drop(columns=['mean', 'std'])
        print("Calculated 'unusual_access' based on department statistics.")
    else:
        df['unusual_access'] = False
        print("Limitation: 'department' column is unavailable in the data. Cannot calculate 'unusual_access' by department. Set to False.")
        
    # Ensure reports directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
    # Save combined results
    df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}\n")
    
    # Show columns, shape, risk-level counts, prediction counts, and 5 sample rows
    print("--- Analysis Results ---")
    print(f"Columns: {list(df.columns)}")
    print(f"Shape: {df.shape}")
    print("\nRisk Level Counts:")
    print(df['risk_level'].value_counts())
    print("\nModel Prediction Counts:")
    print(df['model_prediction'].value_counts())
    print("\n5 Sample Rows:")
    print(df.head(5))

if __name__ == '__main__':
    main()
