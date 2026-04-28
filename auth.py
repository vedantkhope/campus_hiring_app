import streamlit as st
from db import get_admin, get_student_by_credentials, register_student

def init_session():
    for key in ["logged_in", "role", "user_id", "username"]:
        if key not in st.session_state:
            st.session_state[key] = None
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.logged_in = False

def login_admin(username, password):
    admin = get_admin(username, password)
    if admin:
        st.session_state.logged_in = True
        st.session_state.role = "admin"
        st.session_state.user_id = admin["id"]
        st.session_state.username = admin["username"]
        return True
    return False

def login_student(username, password):
    student = get_student_by_credentials(username, password)
    if student:
        st.session_state.logged_in = True
        st.session_state.role = "student"
        st.session_state.user_id = student["id"]
        st.session_state.username = student["username"]
        return True
    return False

def logout():
    for key in ["logged_in", "role", "user_id", "username"]:
        st.session_state[key] = None
    st.session_state.logged_in = False
    st.rerun()

def show_login_page():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0f1f2e 50%, #071a14 100%);
        min-height: 100vh;
    }
    .login-hero {
        text-align: center;
        padding: 3rem 1rem 1rem;
    }
    .login-hero h1 {
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1db97a, #0ef0a0, #1db97a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }
    .login-hero p {
        color: #7a8fa6;
        font-size: 1.1rem;
        font-weight: 300;
    }
    .login-card {
        background: rgba(26, 35, 50, 0.85);
        border: 1px solid rgba(29, 185, 122, 0.2);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 40px rgba(29,185,122,0.05);
        margin: 1rem auto;
    }
    .tab-header {
        font-family: 'Syne', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #1db97a;
        margin-bottom: 1.2rem;
        text-align: center;
    }
    .stTextInput > div > div > input {
        background: rgba(15, 20, 35, 0.8) !important;
        border: 1px solid rgba(29, 185, 122, 0.25) !important;
        border-radius: 10px !important;
        color: #e8eaf0 !important;
        padding: 0.7rem 1rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1db97a !important;
        box-shadow: 0 0 0 2px rgba(29,185,122,0.15) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1db97a, #14a368) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2rem !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.3px !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(29,185,122,0.35) !important;
    }
    .badge {
        display: inline-block;
        background: rgba(29,185,122,0.12);
        border: 1px solid rgba(29,185,122,0.3);
        color: #1db97a;
        border-radius: 20px;
        padding: 0.25rem 0.9rem;
        font-size: 0.78rem;
        font-weight: 500;
        margin-bottom: 1rem;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15,20,35,0.6) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9px !important;
        color: #7a8fa6 !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(29,185,122,0.2) !important;
        color: #1db97a !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-hero">
        <h1>🎓 CampusHire</h1>
        <p>Training & Placement Management System</p>
        <div class="badge">✦ Powered by TNP Department</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["🔐 Admin Login", "🎓 Student Login", "📝 Register"])

        with tab1:
            st.markdown('<div class="tab-header">Admin Portal</div>', unsafe_allow_html=True)
            a_user = st.text_input("Username", key="admin_user", placeholder="Enter admin username")
            a_pass = st.text_input("Password", type="password", key="admin_pass", placeholder="Enter password")
            if st.button("Login as Admin", key="admin_login_btn"):
                if login_admin(a_user, a_pass):
                    st.success("Welcome back, Admin!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            st.caption("Default: admin / admin123")

        with tab2:
            st.markdown('<div class="tab-header">Student Portal</div>', unsafe_allow_html=True)
            s_user = st.text_input("Username", key="stu_user", placeholder="Enter your username")
            s_pass = st.text_input("Password", type="password", key="stu_pass", placeholder="Enter password")
            if st.button("Login as Student", key="student_login_btn"):
                if login_student(s_user, s_pass):
                    st.success("Welcome!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

        with tab3:
            st.markdown('<div class="tab-header">Create Account</div>', unsafe_allow_html=True)
            r_user = st.text_input("Choose Username", key="reg_user", placeholder="Pick a username")
            r_pass = st.text_input("Choose Password", type="password", key="reg_pass", placeholder="Min 6 characters")
            r_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2", placeholder="Repeat password")
            if st.button("Create Account", key="register_btn"):
                if not r_user or not r_pass:
                    st.error("All fields required.")
                elif len(r_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                elif r_pass != r_pass2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register_student(r_user, r_pass)
                    if ok:
                        st.success(msg + " Please login.")
                    else:
                        st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
