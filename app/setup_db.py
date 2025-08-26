import sqlite3

conn = sqlite3.connect("app/app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    logic REAL,
    arts REAL,
    science REAL,
    social REAL,
    commerce REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS parents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    student TEXT,
    categories TEXT
)
""")

conn.commit()
conn.close()
print("✅ Database setup done")
