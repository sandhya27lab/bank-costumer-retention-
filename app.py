import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
st.set_page_config(page_title="Customer Retention Dashboard", layout="wide")
df = pd.read_csv("bank_data.csv")

st.title("🏦 Customer Engagement & Retention Dashboard")
st.markdown("Analyzing churn through engagement and product utilization behavior")

# --- KPI Cards at the top ---
st.header("Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

active_churn = df[df["IsActiveMember"]==1]["Exited"].mean()*100
inactive_churn = df[df["IsActiveMember"]==0]["Exited"].mean()*100
ratio = inactive_churn/active_churn

col1.metric("Engagement Retention Ratio", f"{ratio:.2f}x")
col2.metric("Inactive Churn Rate", f"{inactive_churn:.1f}%")
col3.metric("Active Churn Rate", f"{active_churn:.1f}%")

st.markdown("---")
st.write("More sections coming next...")