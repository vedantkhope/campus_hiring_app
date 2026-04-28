# 🎓 CampusHire – TNP Portal

A Streamlit-based Campus Hiring Management System for Training & Placement Departments.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

## 🔑 Default Login

| Role  | Username | Password  |
|-------|----------|-----------|
| Admin | admin    | admin123  |

Students can register from the login page.

## 📁 Project Structure

```
campus_hiring_app/
├── app.py                   # Main entry point
├── db.py                    # SQLite database + all queries
├── auth.py                  # Login, register, session management
├── utils.py                 # Eligibility logic, file handler, styles, sidebar
├── pages/
│   ├── admin_dashboard.py   # Admin stats + company management
│   ├── admin_students.py    # Applicants view + downloads
│   ├── student_dashboard.py # Student home + applications
│   ├── student_profile.py   # Profile editor
│   ├── student_companies.py # Browse companies + apply
│   └── student_resume.py    # Resume upload/update
├── uploads/resumes/         # Local resume storage
├── campus_hiring.db         # SQLite database (auto-created)
├── .streamlit/config.toml   # Theme configuration
└── requirements.txt
```

## ✨ Features

### Admin
- Dashboard with stats & charts
- Add / Edit / Delete companies
- View applicants per company
- Download applicant data as CSV
- Download student resumes

### Student
- Register & Login
- Create/update profile (Name, Branch, CGPA, Skills)
- Browse companies with eligibility auto-check
- Apply with one click (if eligible)
- Upload/update resume (PDF/DOC/DOCX)
- Track all applications

## 🛠 Tech Stack
- **Frontend + Backend**: Python (Streamlit)
- **Database**: SQLite
- **Charts**: Plotly
- **File Storage**: Local filesystem
