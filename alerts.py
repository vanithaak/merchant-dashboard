# alerts.py
import streamlit as st

def alerts():
    st.markdown("## 🚨 Payment Alerts")
    st.caption("Issues requiring attention")

    with st.container():
        st.error("🔴 ICICI Bank failure rate increased by 18% today")
        st.warning("🟠 Weekend success rate below baseline")
        st.info("🟡 High-value transactions show increased retries")
