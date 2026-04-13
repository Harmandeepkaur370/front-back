import sqlite3

DB_NAME = "hospital.db"

def check_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", tables)

    # Show sample data from each table
    for table in ['users', 'patients', 'analytics']:
        print(f"\nTable: {table}")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No data yet.")

    conn.close()

if __name__ == "__main__":
    check_tables()