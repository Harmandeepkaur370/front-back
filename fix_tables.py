import sqlite3

def fix_tables():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    # Drop old tables to migrate to exact requested name/structure
    cursor.execute("DROP TABLE IF EXISTS patients")
    cursor.execute("DROP TABLE IF EXISTS patient")
    cursor.execute("DROP TABLE IF EXISTS analytics")

    # Patient table (singular - exact user columns)
    cursor.execute("""
        CREATE TABLE patient (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            disease TEXT,
            username TEXT,
            prediction TEXT
        )
    """)

    # Analytics table (exact user columns, NO underscores)
    cursor.execute("""
        CREATE TABLE analytics (
            id INTEGER PRIMARY KEY,
            totalpatients INTEGER DEFAULT 0,
            heartpositive INTEGER DEFAULT 0,
            diabetespositive INTEGER DEFAULT 0
        )
    """)

    # Initialize row 1 for global stats
    cursor.execute("INSERT INTO analytics (id, totalpatients, heartpositive, diabetespositive) VALUES (1, 0, 0, 0)")

    conn.commit()
    conn.close()
    print("Tables 'patient' and 'analytics' have been reset with exact schemas.")

if __name__ == "__main__":
    fix_tables()
