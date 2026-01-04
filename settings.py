# settings.py
import streamlit as st

def settings():
    st.markdown("## ⚙️ Settings")
    st.caption("Manage payment preferences, notifications, risk controls")

    with st.container():
        st.checkbox("Enable email alerts", value=True)
        st.checkbox("Enable SMS notifications")
        st.selectbox("Default report format", ["PDF", "CSV", "Excel"])
