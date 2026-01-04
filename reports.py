# reports.py
import streamlit as st

def reports():
    st.markdown("## 📁 Reports & Exports")
    st.caption("Download summaries for stakeholders")

    with st.container():
        st.button("📄 Download Executive Summary", use_container_width=True)
        st.button("📊 Download Failure Breakdown CSV", use_container_width=True)
