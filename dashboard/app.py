import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Insider Threat Detection Dashboard", layout="wide")

st.title("Insider Threat Detection Dashboard")

@st.cache_data
def load_data():
    file_path = "reports/risk_report.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

df = load_data()

if df is not None:
    st.header("Overview Metrics")
    
    # Calculate metrics
    total_users = len(df)
    suspicious_users = len(df[df['model_prediction'] == 1])
    high_risk = len(df[df['risk_level'] == 'High'])
    medium_risk = len(df[df['risk_level'] == 'Medium'])
    low_risk = len(df[df['risk_level'] == 'Low'])
    
    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Users", total_users)
    col2.metric("Suspicious (Prediction=1)", suspicious_users)
    col3.metric("High Risk", high_risk)
    col4.metric("Medium Risk", medium_risk)
    col5.metric("Low Risk", low_risk)
    
    st.markdown("---")
    
    # Layout for chart and user selection
    row1_col1, row1_col2 = st.columns([1, 2])
    
    with row1_col1:
        st.subheader("Risk Level Distribution")
        risk_counts = df['risk_level'].value_counts().reset_index()
        risk_counts.columns = ['Risk Level', 'Count']
        st.bar_chart(risk_counts.set_index('Risk Level'))
        
    with row1_col2:
        st.subheader("User Details")
        user_list = df['user'].tolist()
        selected_user = st.selectbox("Select a User to view details:", user_list)
        
        if selected_user:
            user_data = df[df['user'] == selected_user].iloc[0]
            
            detail_col1, detail_col2 = st.columns(2)
            with detail_col1:
                st.write(f"**User ID:** {user_data['user']}")
                st.write(f"**Risk Level:** {user_data['risk_level']} (Score: {user_data['risk_score']})")
                st.write(f"**Model Prediction:** {user_data['model_prediction']}")
                st.write(f"**Unusual Access:** {user_data['unusual_access']}")
            with detail_col2:
                st.write(f"**Login Count:** {user_data['login_count']}")
                st.write(f"**After Hours Logins:** {user_data['after_hours_login']}")
                st.write(f"**File Copy Count:** {user_data['file_copy_count']}")
                st.write(f"**USB Connections:** {user_data['usb_connections']}")
    
    st.markdown("---")
    
    st.subheader("Risk Report Data")
    st.write("You can sort and filter the data by clicking on the column headers.")
    
    # Filter by risk level
    risk_filter = st.multiselect("Filter by Risk Level:", options=['High', 'Medium', 'Low'], default=['High', 'Medium', 'Low'])
    filtered_df = df[df['risk_level'].isin(risk_filter)]
    
    st.dataframe(filtered_df, use_container_width=True)
    
else:
    st.error("Report data not found. Please ensure that the risk analysis script has been run and 'reports/risk_report.csv' exists.")
