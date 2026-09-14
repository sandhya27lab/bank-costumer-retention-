import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Retention Dashboard", layout="wide")
df = pd.read_csv("bank_data.csv")

# Clean up column names (remove extra spaces around headers)
df.columns = df.columns.str.strip()

st.title("🏦 Customer Engagement & Retention Dashboard")
st.markdown("Analyzing churn through engagement and product utilization behavior")

# ================= SIDEBAR FILTERS =================
st.sidebar.header("Filters")

engagement_options = df["EngagmentGroup"].dropna().unique().tolist()
selected_engagement = st.sidebar.multiselect(
    "Engagement Group", engagement_options, default=engagement_options
)

product_range = st.sidebar.slider(
    "Number of Products", int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max()),
    (int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max()))
)

balance_range = st.sidebar.slider(
    "Balance Range", float(df["Balance"].min()), float(df["Balance"].max()),
    (float(df["Balance"].min()), float(df["Balance"].max()))
)

# Apply filters
filtered_df = df[
    (df["EngagmentGroup"].isin(selected_engagement)) &
    (df["NumOfProducts"].between(product_range[0], product_range[1])) &
    (df["Balance"].between(balance_range[0], balance_range[1]))
]

st.sidebar.markdown(f"**Showing {len(filtered_df)} of {len(df)} customers**")

# ================= KPI CARDS =================
st.header("Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

active_churn = filtered_df[filtered_df["IsActiveMember"] == 1]["Exited"].mean() * 100
inactive_churn = filtered_df[filtered_df["IsActiveMember"] == 0]["Exited"].mean() * 100
ratio = inactive_churn / active_churn if active_churn > 0 else 0

churn_1prod = filtered_df[filtered_df["NumOfProducts"] == 1]["Exited"].mean() * 100
churn_2prod = filtered_df[filtered_df["NumOfProducts"] == 2]["Exited"].mean() * 100
product_depth_index = churn_1prod - churn_2prod

highbal_customers = filtered_df[filtered_df["HighBalance"] == "HIGH"]
highbal_disengagement_rate = (highbal_customers["IsActiveMember"] == 0).mean() * 100

card_churn = filtered_df[filtered_df["HasCrCard"] == 1]["Exited"].mean() * 100
nocard_churn = filtered_df[filtered_df["HasCrCard"] == 0]["Exited"].mean() * 100
card_stickiness = nocard_churn - card_churn

col1.metric("Engagement Retention Ratio", f"{ratio:.2f}x")
col2.metric("Product Depth Index", f"{product_depth_index:.1f} pts")
col3.metric("High-Balance Disengagement", f"{highbal_disengagement_rate:.1f}%")
col4.metric("Card Stickiness Score", f"{card_stickiness:.1f} pts")
col5.metric("Avg Relationship Score", f"{filtered_df['RelationshipScore'].mean():.1f}")

st.markdown("---")

# ================= CHARTS =================
st.header("Engagement vs Churn Overview")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Churn Rate by Engagement Group")
    churn_by_group = filtered_df.groupby("EngagmentGroup")["Exited"].mean() * 100
    fig1, ax1 = plt.subplots()
    churn_by_group.plot(kind="bar", ax=ax1, color="steelblue")
    ax1.set_ylabel("Churn Rate (%)")
    ax1.set_xlabel("")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig1)

with col_b:
    st.subheader("Churn Rate by Number of Products")
    churn_by_product = filtered_df.groupby("NumOfProducts")["Exited"].mean() * 100
    fig2, ax2 = plt.subplots()
    churn_by_product.plot(kind="bar", ax=ax2, color="indianred")
    ax2.set_ylabel("Churn Rate (%)")
    ax2.set_xlabel("Number of Products")
    st.pyplot(fig2)

st.markdown("---")

# ================= RELATIONSHIP SCORE TREND =================
st.header("Relationship Strength vs Churn")
score_churn = filtered_df.groupby("RelationshipScore")["Exited"].mean() * 100
fig3, ax3 = plt.subplots()
score_churn.plot(kind="line", marker="o", ax=ax3, color="seagreen")
ax3.set_ylabel("Churn Rate (%)")
ax3.set_xlabel("Relationship Score")
st.pyplot(fig3)

st.markdown("---")

# ================= AT-RISK CUSTOMERS TABLE =================
st.header("⚠️ High-Value Disengaged Customer Detector")
at_risk = filtered_df[filtered_df["AtRiskPremium"] == "YES"].sort_values("Balance", ascending=False)
st.write(f"Found **{len(at_risk)}** at-risk premium customers")
st.dataframe(
    at_risk[["CustomerId", "Balance", "EstimatedSalary", "NumOfProducts", "IsActiveMember"]].head(50)
)
