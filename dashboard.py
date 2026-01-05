import streamlit as st
import pandas as pd
import plotly.express as px


# ---------- Helpers ----------
@st.cache_data
def load_sample_data(name: str):
    if name == "Sample: Razorpay":
        return pd.read_csv("data/sample_razorpay.csv")
    if name == "Sample: PayU":
        return pd.read_csv("data/sample_payu.csv")
    return None


def set_active_df(df, source_name):
    st.session_state["active_df"] = df
    st.session_state["data_source"] = source_name


# ---------- Dashboard ----------
def dashboard():
    st.markdown("## Payment Reliability Dashboard")
    st.caption("Visual insights into transaction success, failures, and risk patterns")

    st.divider()

    # ---------- Global Dataset Selector ----------
    col1, col2 = st.columns([3, 2])

    with col1:
        dataset_choice = st.selectbox(
            "Dataset",
            [
                "Select dataset",
                "Sample: Razorpay",
                "Sample: PayU",
                "Upload new CSV"
            ],
            label_visibility="collapsed"
        )

    with col2:
        if "data_source" in st.session_state:
            st.metric("Active Dataset", st.session_state["data_source"])

    # ---------- Dataset Logic ----------
    if dataset_choice.startswith("Sample"):
        df = load_sample_data(dataset_choice)
        set_active_df(df, dataset_choice)

    elif dataset_choice == "Upload new CSV":
        uploaded_file = st.file_uploader(
            "Upload payment CSV",
            type=["csv"],
            help="Expected columns: date, bank, status, amount"
        )
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            set_active_df(df, "Uploaded CSV")

    # ---------- Empty State ----------
    if "active_df" not in st.session_state:
        st.info("👆 Select a dataset or upload a CSV to begin analysis.")
        return

    df = st.session_state["active_df"].copy()
    df["date"] = pd.to_datetime(df["date"])

    st.divider()

    # ---------- KPI ROW ----------
    total_txns = len(df)
    success_rate = round((df["status"] == "SUCCESS").mean() * 100, 2)
    failure_rate = round(100 - success_rate, 2)
    total_value = int(df["amount"].sum())

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Transactions", f"{total_txns:,}")
    k2.metric("Success Rate", f"{success_rate}%")
    k3.metric("Failure Rate", f"{failure_rate}%")
    k4.metric("Total Value", f"₹{total_value:,}")

    st.divider()

    # ---------- Volume Trend ----------
    st.subheader("📈 Transaction Volume Trend")

    volume_df = (
        df.groupby(["date", "status"])
        .size()
        .reset_index(name="count")
    )

    volume_chart = px.line(
        volume_df,
        x="date",
        y="count",
        color="status",
        markers=True
    )

    st.plotly_chart(volume_chart, use_container_width=True)

    # ---------- Success Rate Trend ----------
    st.subheader("📉 Success Rate Trend")

    rate_df = (
        df.assign(success=df["status"] == "SUCCESS")
          .groupby("date")["success"]
          .mean()
          .reset_index()
    )
    rate_df["success_rate"] = rate_df["success"] * 100

    rate_chart = px.line(
        rate_df,
        x="date",
        y="success_rate",
        markers=True
    )

    st.plotly_chart(rate_chart, use_container_width=True)

    st.divider()

    # ---------- Amount Distribution ----------
    st.subheader("💰 Transaction Amount Distribution")

    amount_chart = px.histogram(
        df,
        x="amount",
        nbins=30
    )

    st.plotly_chart(amount_chart, use_container_width=True)

    st.divider()

    # ---------- Bank-wise Success Rate ----------
    st.subheader("🏦 Bank-wise Success Rate")

    bank_success_df = (
        df.groupby("bank")
        .apply(lambda x: (x["status"] == "SUCCESS").mean() * 100)
        .reset_index(name="success_rate")
        .sort_values("success_rate")
    )

    bank_success_chart = px.bar(
        bank_success_df,
        x="success_rate",
        y="bank",
        orientation="h"
    )

    st.plotly_chart(bank_success_chart, use_container_width=True)

    # ---------- Failure Rate by Bank ----------
    st.subheader("🚫 Failure Rate by Bank")

    bank_failure_df = (
        df.assign(failed=df["status"] != "SUCCESS")
        .groupby("bank")["failed"]
        .mean()
        .reset_index()
    )
    bank_failure_df["failure_rate"] = bank_failure_df["failed"] * 100

    bank_failure_chart = px.bar(
        bank_failure_df.sort_values("failure_rate"),
        x="failure_rate",
        y="bank",
        orientation="h"
    )

    st.plotly_chart(bank_failure_chart, use_container_width=True)

    st.divider()

    # ---------- Bank × Status Heatmap ----------
    st.subheader("🔥 Bank vs Status Heatmap")

    heatmap_df = (
        df.groupby(["bank", "status"])
        .size()
        .reset_index(name="count")
    )

    heatmap_chart = px.density_heatmap(
        heatmap_df,
        x="status",
        y="bank",
        z="count",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(heatmap_chart, use_container_width=True)

    st.divider()

    # ---------- High-Value Failure Risk ----------
    st.subheader("⚠️ High-Value Failed Transactions")

    threshold = df["amount"].quantile(0.9)
    high_value_failures = df[
        (df["status"] != "SUCCESS") & (df["amount"] > threshold)
    ]

    if high_value_failures.empty:
        st.success("🎉 No high-value failures detected")
    else:
        st.dataframe(
            high_value_failures[["date", "bank", "amount", "status"]],
            use_container_width=True
        )
