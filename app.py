# app.py
import streamlit as st
from login import login
from dashboard import dashboard
from alerts import alerts
from reports import reports
from settings import settings
from upload import upload

st.set_page_config(
    page_title="Merchant Payment Reliability Platform",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Session Init ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------- Login ----------
if not st.session_state.logged_in:
    login()
else:
    # ---------- Sidebar ----------
    st.sidebar.markdown("## 💳 Merchant Console")
    st.sidebar.caption(st.session_state.merchant_email)
    st.sidebar.divider()

    module = st.sidebar.radio(
        "Select Module",
        ["📊 Dashboard", "🚨 Alerts", "📁 Reports", "📤 Upload", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    st.sidebar.divider()
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # ---------- Module Routing ----------
    if module == "📊 Dashboard":
        dashboard()
    elif module == "🚨 Alerts":
        alerts()
    elif module == "📁 Reports":
        reports()
    elif module == "📤 Upload":
        upload()
    elif module == "⚙️ Settings":
        settings()
