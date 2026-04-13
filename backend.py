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

    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            disease_type TEXT,
            predicted TEXT
        )
    """)

    conn.commit()
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

    # Assuming you store username in patients table
    cursor.execute(
        "SELECT name, age, disease, prediction FROM patients WHERE username=?",
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
    