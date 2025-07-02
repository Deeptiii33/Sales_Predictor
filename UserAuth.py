import sqlite3
import streamlit as st
import bcrypt
import re
from sales_predictor import sales_predictor

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Authenticate user based on credentials
def authenticate_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user:
        stored_hashed_password = user['password']
        # Check if entered password matches the hashed password in the database
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return user
    return None

# Password strength evaluation
def evaluate_password_strength(password):
    strength = "Weak"
    if len(password) >= 6:
        if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"\d", password) and re.search(r"[@$!%*#?&]", password):
            strength = "Strong"
        elif re.search(r"[a-z]", password) and re.search(r"\d", password):
            strength = "Moderate"
    return strength

# Validate username and password (at least one letter, one number, and one special character)
def validate_credentials(username, password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$"
    return bool(re.match(pattern, username) and re.match(pattern, password))

# Register new user (signup functionality)
def signup(username, password):
    if not validate_credentials(username, password):
        st.error("Both username and password must contain at least one letter, one number, one special character, and be at least 6 characters long.")
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password.decode('utf-8')))
        conn.commit()
        conn.close()
        st.success("Account created successfully! Please log in.")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.page = "Login"

# Define the login function
def login(username, password):
    user = authenticate_user(username, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.username = user['username']
        st.session_state.page = "Dashboard"
    else:
        st.error("Invalid credentials. Please try again.")

# App layout
st.title("Streamlit Sales Predictor")

if st.session_state.logged_in:
    if st.session_state.page == "Dashboard":
        st.subheader(f"Welcome to your Dashboard, {st.session_state.username}!")
        st.write("This is your dashboard.")
        if st.button("Go to Sales Predictor"):
            st.session_state.page = "Sales Predictor"
    elif st.session_state.page == "Sales Predictor":
        sales_predictor()
else:
    menu = st.sidebar.selectbox('Menu', ['Login', 'Sign Up'])
    
    if menu == 'Login':
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(username, password)

    elif menu == 'Sign Up':
        st.subheader("Sign Up")
        signup_username = st.text_input("New Username")
        signup_password = st.text_input("New Password", type="password")
        strength = evaluate_password_strength(signup_password)
        st.write("Password strength: ", strength)
        if st.button("Create Account"):
            signup(signup_username, signup_password)

