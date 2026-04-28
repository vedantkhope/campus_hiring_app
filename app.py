import streamlit as st
from db import init_db
from auth import init_session, show_login_page
from utils import global_styles, sidebar_nav

# Page config
st.set_page_config(
    page_title="CampusHire – TNP Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Init DB
init_db()

# Init session
init_session()

# Global styles
global_styles()

# Route
if not st.session_state.logged_in:
    show_login_page()
else:
    role = st.session_state.role
    user_id = st.session_state.user_id
    username = st.session_state.username

    sidebar_nav(role, username)

    page = st.session_state.get("page", "dashboard")

    if role == "admin":
        from pages import admin_dashboard, admin_students
        if page == "dashboard":
            admin_dashboard.show()
        elif page == "companies":
            admin_dashboard.show()
        elif page == "students":
            admin_students.show()
        elif page == "downloads":
            admin_students.show_downloads()
        else:
            admin_dashboard.show()

    elif role == "student":
        from pages import student_dashboard, student_profile, student_companies, student_resume
        if page == "dashboard":
            student_dashboard.show(user_id)
        elif page == "profile":
            student_profile.show(user_id)
        elif page == "companies":
            student_companies.show(user_id)
        elif page == "resume":
            student_resume.show(user_id)
        else:
            student_dashboard.show(user_id)
