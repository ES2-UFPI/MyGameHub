import streamlit as st
import login as login
import profile
from login import login_page

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if st.session_state.page == 'login':
        login.login_page()
    elif st.session_state.page == 'profile':
        profile.profile_page()

if __name__ == "__main__":
    main()