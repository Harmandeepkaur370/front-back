import sqlite3

# Connect to SQLite database (creates hospital.db if not exists)
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# -----------------------------
# Users table
# -----------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

# -----------------------------
# Patients table
# -----------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    disease_type TEXT,       -- "heart" or "diabetes"
    predicted_positive INTEGER, -- 0 or 1
    date TEXT
)
''')

# -----------------------------
# Analytics table (optional)
# -----------------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_patients INTEGER DEFAULT 0,
    heart_positive INTEGER DEFAULT 0,
    diabetes_positive INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()
print("Database and tables created successfully!")