# Insider Threat Detection System

## Problem Statement
Detecting insider threats within an organization is challenging due to the massive volume of normal user activity. This project aims to build an end-to-end Machine Learning solution to identify suspicious behavior, flag unusual access patterns, and provide a holistic risk score for each user. By leveraging logs from various sources (devices, files, logins), we can proactively detect potential security incidents before they cause significant harm.

## Project Architecture & Workflow
1. **Data Loading & Preprocessing:** Load raw logs (device, logon, file) and handle missing/inconsistent data.
2. **Feature Engineering:** Aggregate user activity into a comprehensive feature table (e.g., after-hours logins, file copy counts, USB connections).
3. **Model Training:** Train a Random Forest Classifier on the engineered features to identify malicious behavior.
4. **Risk Analysis layer:** Calculate a rule-based risk score based on model predictions and specific activity thresholds (e.g., heavy file copying, unusual access).
5. **Dashboard:** Provide an interactive Streamlit UI for security analysts to explore users, view risk levels, and investigate anomalous behaviors.

## Project Structure
```text
.
├── dashboard/
│   └── app.py                  # Streamlit dashboard application
├── data/
│   └── processed/              # Processed data files and feature table
├── models/
│   └── random_forest_model.pkl # Trained Random Forest model
├── reports/
│   └── risk_report.csv         # Final risk analysis report
├── src/
│   ├── load_data.py            # Data loading utilities
│   ├── preprocess.py           # Data cleaning and preprocessing logic
│   ├── feature_engineering.py  # Feature extraction script
│   ├── train_model.py          # Model training and evaluation script
│   └── risk_analysis.py        # Risk scoring and unusual access calculation
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

## Setup & Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repo-url>
   cd insider-threat-detection-ml
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. **Preprocessing:** Clean raw data.
   ```bash
   python src/preprocess.py
   ```
2. **Feature Engineering:** Generate the feature table.
   ```bash
   python src/feature_engineering.py
   ```
3. **Training:** Train the model and evaluate it.
   ```bash
   python src/train_model.py
   ```
4. **Risk Analysis:** Calculate user risk scores and unusual access flags.
   ```bash
   python src/risk_analysis.py
   ```
5. **Dashboard:** Launch the Streamlit web application.
   ```bash
   streamlit run dashboard/app.py
   ```

## Model Evaluation Metrics
The Random Forest Classifier achieved the following performance metrics on the test set:
- **Accuracy:** 1.0000
- **Precision:** 1.0000
- **Recall:** 1.0000
- **F1 Score:** 1.0000

## Day 5 Risk Results
Out of 1000 users analyzed:
- **Low Risk:** 738 users
- **Medium Risk:** 191 users
- **High Risk:** 71 users
- **Suspicious (Model Prediction = 1):** 71 users

## Limitations
- **Unavailable Department Data:** The processed data does not currently contain a `department` attribute for users. Consequently, the "Unusual Access" rule (comparing file access to department averages) cannot be fully calculated and defaults to `False` to avoid inventing data.

## Dashboard
![Dashboard Screenshot Placeholder](dashboard_screenshot.png)
*(Instructions: Replace `dashboard_screenshot.png` with an actual screenshot of the Streamlit dashboard running locally)*
