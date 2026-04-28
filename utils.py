import os
import streamlit as st

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads", "resumes")
os.makedirs(UPLOAD_DIR, exist_ok=True)

BRANCHES = ["CSE", "IT", "ECE", "EEE", "MECH", "CIVIL", "AIDS", "AIML", "CSD", "Other"]

def check_eligibility(student, company):
    reasons = []
    eligible = True

    if student.get("cgpa") is None or student.get("branch") is None:
        return False, ["Complete your profile first."]

    if student["cgpa"] < company["min_cgpa"]:
        eligible = False
        reasons.append(f"CGPA {student['cgpa']} < required {company['min_cgpa']}")

    allowed = [b.strip() for b in company["eligible_branches"].split(",")]
    if "All" not in allowed and student["branch"] not in allowed:
        eligible = False
        reasons.append(f"Branch {student['branch']} not eligible")

    return eligible, reasons

def save_resume(student_id, file):
    allowed = ["pdf", "doc", "docx"]
    ext = file.name.split(".")[-1].lower()
    if ext not in allowed:
        return None, "Only PDF, DOC, DOCX allowed."
    if file.size > 5 * 1024 * 1024:
        return None, "File too large (max 5MB)."
    filename = f"student_{student_id}_{file.name}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(file.getbuffer())
    return path, "Resume uploaded!"

def global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .stApp {
        background: linear-gradient(160deg, #0a0e1a 0%, #0d1a14 60%, #080d18 100%);
    }
    section[data-testid="stSidebar"] {
        background: rgba(10, 15, 28, 0.95) !important;
        border-right: 1px solid rgba(29,185,122,0.15) !important;
    }
    .metric-card {
        background: rgba(26, 35, 50, 0.7);
        border: 1px solid rgba(29,185,122,0.2);
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: all 0.2s;
    }
    .metric-card:hover {
        border-color: rgba(29,185,122,0.5);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(29,185,122,0.1);
    }
    .metric-card .metric-val {
        font-family: 'Syne', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #1db97a;
    }
    .metric-card .metric-label {
        color: #7a8fa6;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .page-title {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #e8eaf0;
        margin-bottom: 0.2rem;
    }
    .page-subtitle {
        color: #7a8fa6;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .company-card {
        background: rgba(22, 30, 46, 0.8);
        border: 1px solid rgba(29,185,122,0.15);
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    .company-card:hover {
        border-color: rgba(29,185,122,0.4);
        box-shadow: 0 6px 25px rgba(29,185,122,0.08);
    }
    .company-name {
        font-family: 'Syne', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: #e8eaf0;
    }
    .company-role {
        color: #1db97a;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .pill {
        display: inline-block;
        background: rgba(29,185,122,0.12);
        border: 1px solid rgba(29,185,122,0.25);
        color: #1db97a;
        border-radius: 20px;
        padding: 0.2rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 500;
        margin: 0.1rem;
    }
    .pill-red {
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.25);
        color: #f87171;
    }
    .pill-yellow {
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(251,191,36,0.25);
        color: #fbbf24;
    }
    .section-header {
        font-family: 'Syne', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #1db97a;
        border-bottom: 1px solid rgba(29,185,122,0.2);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    div[data-testid="stForm"] {
        background: rgba(22,30,46,0.6);
        border: 1px solid rgba(29,185,122,0.15);
        border-radius: 16px;
        padding: 1.5rem;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stTextArea > div > div > textarea {
        background: rgba(10,14,26,0.8) !important;
        border: 1px solid rgba(29,185,122,0.2) !important;
        border-radius: 10px !important;
        color: #e8eaf0 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1db97a, #14a368) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(29,185,122,0.3) !important;
    }
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    div[data-testid="stExpander"] {
        background: rgba(22,30,46,0.5);
        border: 1px solid rgba(29,185,122,0.15) !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def sidebar_nav(role, username):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 1rem 0; border-bottom: 1px solid rgba(29,185,122,0.2); margin-bottom: 1rem;">
            <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:800;
                        background:linear-gradient(135deg,#1db97a,#0ef0a0);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                🎓 CampusHire
            </div>
            <div style="color:#7a8fa6; font-size:0.8rem; margin-top:0.2rem;">
                {'🔑 Admin' if role=='admin' else '👤 Student'} · {username}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if role == "admin":
            pages = {
                "📊 Dashboard": "dashboard",
                "🏢 Manage Companies": "companies",
                "👥 View Students": "students",
                "📥 Downloads": "downloads",
            }
        else:
            pages = {
                "🏠 Dashboard": "dashboard",
                "👤 My Profile": "profile",
                "🏢 Companies": "companies",
                "📄 My Resume": "resume",
            }

        if "page" not in st.session_state:
            st.session_state.page = "dashboard"

        for label, key in pages.items():
            active = st.session_state.page == key
            btn_style = "primary" if active else "secondary"
            if st.button(label, key=f"nav_{key}", use_container_width=True, type=btn_style):
                st.session_state.page = key
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            from auth import logout
            logout()
