# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

def dashboard():
    st.markdown("## 📊 Merchant Payment Reliability")
    st.caption("Live payment performance based on uploaded data")

    if "txn_data" not in st.session_state:
        st.info("📤 Upload transaction data to view dashboard")
        return

    df = st.session_state.txn_data.copy()

    # ---------- METRICS ----------
    total_txns = len(df)
    success_txns = len(df[df["status"] == "success"])
    failure_txns = len(df[df["status"] == "failure"])

    success_rate = round((success_txns / total_txns) * 100, 1)
    failure_rate = round((failure_txns / total_txns) * 100, 1)
    avg_retry = round(df["retry_count"].mean(), 1)

    # ---------- KPI CARDS ----------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Success Rate", f"{success_rate}%")
    c2.metric("Failure Rate", f"{failure_rate}%")
    c3.metric("Avg Retry Count", avg_retry)
    c4.metric("Total Transactions", total_txns)

    st.divider()

    # ---------- DAILY TRENDS ----------
    daily = df.groupby(
        df["date"].dt.date
    ).agg(
        success_rate=("status", lambda x: (x == "success").mean() * 100),
        failure_rate=("status", lambda x: (x == "failure").mean() * 100),
        retry_count=("retry_count", "mean")
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(
            daily,
            x="date",
            y=["success_rate", "failure_rate"],
            markers=True,
            title="Success vs Failure Trend (%)"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(
            daily,
            x="date",
            y="retry_count",
            markers=True,
            title="Average Retry Count Trend"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ---------- PEER COMPARISON ----------
    peer = df.groupby("bank").agg(
        success_rate=("status", lambda x: (x == "success").mean() * 100),
        txns=("status", "count")
    ).reset_index()

    fig3 = px.bar(
        peer,
        x="bank",
        y="success_rate",
        text=peer["success_rate"].round(1),
        title="Success Rate by Bank (%)"
    )
    fig3.update_traces(texttemplate="%{text}%", textposition="outside")
    fig3.update_layout(yaxis_range=[0, 100])

    st.plotly_chart(fig3, use_container_width=True)

    # ---------- INSIGHTS ----------
    st.divider()
    st.markdown("### 🔍 Key Insights")

    worst_bank = peer.sort_values("success_rate").iloc[0]
    best_bank = peer.sort_values("success_rate").iloc[-1]

    st.warning(f"⚠ Lowest success rate: {worst_bank['bank']} ({worst_bank['success_rate']:.1f}%)")
    st.success(f"✔ Best performing bank: {best_bank['bank']} ({best_bank['success_rate']:.1f}%)")
