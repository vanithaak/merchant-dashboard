# upload.py
import streamlit as st
import pandas as pd

def upload():
    st.markdown("## 📤 Upload Transaction Data")
    st.caption("Upload payment transaction CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)

            required_cols = {"date", "bank", "amount", "status", "retry_count"}
            if not required_cols.issubset(df.columns):
                st.error("CSV format invalid. Missing required columns.")
                return

            df["date"] = pd.to_datetime(df["date"])

            # 🔥 Store in session_state
            st.session_state.txn_data = df

            st.success("Transaction data uploaded successfully!")
            st.dataframe(df.head(), use_container_width=True)

        except Exception as e:
            st.error(f"Upload failed: {e}")
