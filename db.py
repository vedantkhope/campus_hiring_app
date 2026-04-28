import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "campus_hiring.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            email TEXT UNIQUE,
            branch TEXT,
            cgpa REAL,
            skills TEXT,
            phone TEXT,
            resume_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            job_role TEXT NOT NULL,
            package REAL,
            min_cgpa REAL,
            eligible_branches TEXT,
            required_skills TEXT,
            hiring_date TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Applied',
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (company_id) REFERENCES companies(id),
            UNIQUE(student_id, company_id)
        )
    """)

    # Seed default admin
    c.execute("SELECT * FROM admins WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ("admin", "admin123"))

    conn.commit()
    conn.close()

# ── AUTH ──────────────────────────────────────────────────────────────────────

def get_admin(username, password):
    conn = get_conn()
    row = conn.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_student_by_credentials(username, password):
    conn = get_conn()
    row = conn.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password)).fetchone()
    conn.close()
    return dict(row) if row else None

def register_student(username, password):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO students (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True, "Registered successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def get_student_by_id(student_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

# ── STUDENT PROFILE ───────────────────────────────────────────────────────────

def update_student_profile(student_id, name, email, branch, cgpa, skills, phone):
    conn = get_conn()
    conn.execute("""
        UPDATE students SET name=?, email=?, branch=?, cgpa=?, skills=?, phone=?
        WHERE id=?
    """, (name, email, branch, float(cgpa), skills, phone, student_id))
    conn.commit()
    conn.close()

def update_resume_path(student_id, path):
    conn = get_conn()
    conn.execute("UPDATE students SET resume_path=? WHERE id=?", (path, student_id))
    conn.commit()
    conn.close()

# ── COMPANIES ─────────────────────────────────────────────────────────────────

def add_company(name, job_role, package, min_cgpa, eligible_branches, required_skills, hiring_date, description):
    conn = get_conn()
    conn.execute("""
        INSERT INTO companies (name, job_role, package, min_cgpa, eligible_branches, required_skills, hiring_date, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, job_role, float(package), float(min_cgpa), eligible_branches, required_skills, hiring_date, description))
    conn.commit()
    conn.close()

def get_all_companies():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM companies ORDER BY hiring_date ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_company_by_id(company_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM companies WHERE id=?", (company_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_company(company_id, name, job_role, package, min_cgpa, eligible_branches, required_skills, hiring_date, description):
    conn = get_conn()
    conn.execute("""
        UPDATE companies SET name=?, job_role=?, package=?, min_cgpa=?, eligible_branches=?,
        required_skills=?, hiring_date=?, description=? WHERE id=?
    """, (name, job_role, float(package), float(min_cgpa), eligible_branches, required_skills, hiring_date, description, company_id))
    conn.commit()
    conn.close()

def delete_company(company_id):
    conn = get_conn()
    conn.execute("DELETE FROM applications WHERE company_id=?", (company_id,))
    conn.execute("DELETE FROM companies WHERE id=?", (company_id,))
    conn.commit()
    conn.close()

# ── APPLICATIONS ──────────────────────────────────────────────────────────────

def apply_to_company(student_id, company_id):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO applications (student_id, company_id) VALUES (?, ?)", (student_id, company_id))
        conn.commit()
        return True, "Applied successfully!"
    except sqlite3.IntegrityError:
        return False, "Already applied."
    finally:
        conn.close()

def get_student_applications(student_id):
    conn = get_conn()
    rows = conn.execute("""
        SELECT c.*, a.status, a.applied_at FROM applications a
        JOIN companies c ON a.company_id = c.id
        WHERE a.student_id=?
        ORDER BY a.applied_at DESC
    """, (student_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_applications_for_company(company_id):
    conn = get_conn()
    rows = conn.execute("""
        SELECT s.id, s.name, s.email, s.branch, s.cgpa, s.skills, s.phone, s.resume_path, a.status, a.applied_at
        FROM applications a JOIN students s ON a.student_id = s.id
        WHERE a.company_id=?
        ORDER BY s.cgpa DESC
    """, (company_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_students():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ── DASHBOARD STATS ───────────────────────────────────────────────────────────

def get_admin_stats():
    conn = get_conn()
    total_companies = conn.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_applications = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    upcoming = conn.execute("SELECT COUNT(*) FROM companies WHERE hiring_date >= date('now')").fetchone()[0]
    conn.close()
    return {
        "total_companies": total_companies,
        "total_students": total_students,
        "total_applications": total_applications,
        "upcoming_drives": upcoming
    }

def get_applications_per_company():
    conn = get_conn()
    rows = conn.execute("""
        SELECT c.name, COUNT(a.id) as count FROM companies c
        LEFT JOIN applications a ON c.id = a.company_id
        GROUP BY c.id ORDER BY count DESC LIMIT 10
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def has_applied(student_id, company_id):
    conn = get_conn()
    row = conn.execute("SELECT id FROM applications WHERE student_id=? AND company_id=?", (student_id, company_id)).fetchone()
    conn.close()
    return row is not None
