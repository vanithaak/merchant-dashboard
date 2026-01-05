import streamlit as st

def login():
    # Page title
    st.markdown(
        "<h2 style='text-align:center;'>Merchant Payments Console</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:gray;'>Sign in to monitor and improve your payment performance</p>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:red;'>You can enter any mail and password</p>",
        unsafe_allow_html=True
    )

    #st.markdown("<br><br>", unsafe_allow_html=True)

    # Centered container using columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.container(border=True):
            email = st.text_input(
                "Work Email",
                placeholder="name@company.com"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Sign In", use_container_width=True):
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.merchant_email = email
                    st.rerun()
                else:
                    st.error("Please enter your credentials")
