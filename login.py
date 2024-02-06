import streamlit as st
# Define hardcoded username and password
CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "password123"
def main():
    st.title("Login Page")
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    # Get username and password input from the user
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    # Check if username and password are correct
    if st.button("Login"):
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            st.session_state.logged_in = True
    if st.session_state.logged_in:
        display_login_success()
def display_login_success():
    st.title("Login Successful!")
    st.write("Welcome to the Homepage!")
if __name__ == "__main__":
    main()