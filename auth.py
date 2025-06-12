import streamlit as st

def login():
    PASSWORD = st.secrets["auth"]["password"]

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center;'>🔐</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'> Santo y Seña! </h3>", unsafe_allow_html=True)

        password_input = st.text_input("", type="password")
        if st.button("Let's go"):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
            else:
                st.error("Contraseña incorrecta")
        return False

    return True
