# backend.py
import sqlite3
import os
print("DB PATH:", os.path.abspath("hospital.db"))
# ==========================
# DATABASE INITIALIZATION
# ==========================
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Patient table (Singular - Exact Columns)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            disease TEXT,
            username TEXT,
            prediction TEXT
        )
    """)

    # History table (For sidebar visibility)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            name TEXT,
            age INTEGER,
            disease TEXT,
            risk TEXT,
            time TEXT,
            prediction TEXT
        )
    """)

    # Reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            patient_name TEXT,
            disease TEXT,
            file_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Analytics table (Exact Columns, no underscores)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY,
            totalpatients INTEGER DEFAULT 0,
            heartpositive INTEGER DEFAULT 0,
            diabetespositive INTEGER DEFAULT 0
        )
    """)

    # Initialize analytics row 1 if not exists
    cursor.execute("SELECT COUNT(*) FROM analytics WHERE id = 1")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO analytics (id, totalpatients, heartpositive, diabetespositive) VALUES (1, 0, 0, 0)")

    conn.commit()
    conn.close()

# ==========================
# UNIFIED DATA PIPELINE
# ==========================

def update_all_data(user, name, age, disease, risk, prediction, file_path):
    import datetime
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    
    try:
        # ✅ Issue 1: patient Table Update
        cursor.execute("""
            INSERT INTO patient (name, age, disease, username, prediction)
            VALUES (?, ?, ?, ?, ?)
        """, (name, age, disease, user, prediction))

        # ✅ History Table Update (internal use)
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("""
            INSERT INTO history (username, name, age, disease, risk, time, prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user, name, age, disease, risk, time_now, prediction))

        # ✅ Reports Table Update
        cursor.execute("""
            INSERT INTO reports (username, patient_name, disease, file_path, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user, name, disease, file_path))

        # ✅ Issue 2: analytics Table Update
        # Standardize disease name for logic
        d_type = "heart" if "heart" in disease.lower() else "diabetes" if "diabetes" in disease.lower() else ""
        
        cursor.execute("""
            UPDATE analytics
            SET 
              totalpatients = totalpatients + 1,
              heartpositive = heartpositive + CASE 
                  WHEN ? = 'heart' AND ? = 'positive' THEN 1 ELSE 0 END,
              diabetespositive = diabetespositive + CASE 
                  WHEN ? = 'diabetes' AND ? = 'positive' THEN 1 ELSE 0 END
            WHERE id = 1
        """, (d_type, prediction, d_type, prediction))

        conn.commit()
        print(f"✅ Data consistent for {name}. All tables updated.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Database error: {e}")
    finally:
        conn.close()

# ==========================
# USER FUNCTIONS
# ==========================
def add_user(username, password):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"User '{username}' added successfully.")
    else:
        print(f"User '{username}' already exists.")
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
import sqlite3

def signup(username, password):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return "Signup successful ✅"
    except sqlite3.IntegrityError:
        return "User already exists ❌"
    finally:
        conn.close()
import sqlite3

import gradio as gr
import sqlite3

# Database connection
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Login function
def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    if result:
        return f"Login successful! Welcome {username}"
    else:
        return "Invalid username or password"

def save_history(username, name, age, disease, prediction):
    import sqlite3
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO patients (username, name, age, disease, prediction)
        VALUES (?, ?, ?, ?, ?)
    """, (username, name, age, disease, prediction))

    conn.commit()
    conn.close()
# def save_history(name, age, disease, prediction):
#     import sqlite3
#     conn = sqlite3.connect("hospital.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS history (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         age INTEGER,
#         disease TEXT,
#         prediction TEXT
#     )
#     """)

#     cursor.execute(
#         "INSERT INTO history (name, age, disease, prediction) VALUES (?, ?, ?, ?)",
#         (name, age, disease, prediction)
#     )

#     conn.commit()
#     conn.close()
# ==========================
# PATIENT FUNCTIONS
# ==========================
def add_patient(name, age, gender, disease_type, predicted):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age, gender, disease_type, predicted) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, disease_type, predicted)
    )
    conn.commit()
    conn.close()
    print(f"Patient '{name}' added successfully.")

def get_all_patients():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return patients
import sqlite3

def save_patient(name, age, disease, prediction):
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    print("SAVING:", name, age, disease, prediction)  # DEBUG

    cursor.execute(
        "INSERT INTO patients (name, age, disease, prediction) VALUES (?, ?, ?, ?)",
        (name, age, disease, prediction)
    )

    conn.commit()
    conn.close()
def get_history(user):
    import sqlite3
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    # Fetching from the new history table
    cursor.execute(
        "SELECT name, age, disease, risk FROM history WHERE username=? ORDER BY id DESC",
        (user,)
    )
    data = cursor.fetchall()
    conn.close()
    return data
# ==========================
# ANALYTICS
# ==========================
def show_analytics():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT disease_type, COUNT(*) FROM patients GROUP BY disease_type")
    result = cursor.fetchall()
    conn.close()
    print("=== Disease Analytics ===")
    for disease, count in result:
        print(f"{disease}: {count} patient(s)")
    return result

# ==========================
# INITIAL SETUP
# ==========================
if __name__ == "__main__":
    init_db()  # make sure tables exist
    add_user("admin", "1234")  # safely add admin
    print("Backend is ready!")
    