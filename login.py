# login.py
import streamlit as st

def login():
    st.markdown("## Welcome to Merchant Payments Console")
    st.caption("Sign in to monitor and improve your payment performance")

    with st.container():
        email = st.text_input("Work Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign In", use_container_width=True):
            if email and password:
                st.session_state.logged_in = True
                st.session_state.merchant_email = email
                st.rerun()
            else:
                st.error("Please enter your credentials")
