import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Wallet Credit Scoring Dashboard", layout="wide")

# --------- Title --------- #
st.title("📊 Wallet Credit Scoring Dashboard (ML Enhanced)")

# --------- File Upload --------- #
uploaded_file = st.file_uploader("wallet_scores_final.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --------- Basic Stats --------- #
    st.subheader("Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔢 Total Wallets", f"{len(df):,}")
    col2.metric("💯 Average Score", round(df['ml_predicted_score'].mean(), 2))
    col3.metric("💰 Max Deposit (USD)", round(df['total_deposit'].max(), 2))
    col4.metric("⚠️ Liquidated Wallets", df['liquidated'].sum())

    # --------- Score Distribution Plot --------- #
    st.subheader("📈 Credit Score Distribution")
    fig = px.histogram(df, x="ml_predicted_score", nbins=30, color="credit_tier", title="Predicted Credit Score Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # --------- Filter & Search --------- #
    st.subheader("🔎 Wallet Filter")
    tier_filter = st.multiselect("Filter by Credit Tier", options=df['credit_tier'].unique(), default=df['credit_tier'].unique())
    search_wallet = st.text_input("Search by Wallet Address")

    filtered_df = df[df['credit_tier'].isin(tier_filter)]
    if search_wallet:
        filtered_df = filtered_df[filtered_df['wallet'].str.contains(search_wallet, case=False)]

    st.dataframe(filtered_df[['wallet', 'ml_predicted_score', 'credit_tier', 'ml_behavior_reason']], use_container_width=True)

    # --------- Download Button --------- #
    st.download_button("📥 Download Filtered Results", data=filtered_df.to_csv(index=False), file_name="filtered_wallet_scores.csv")
