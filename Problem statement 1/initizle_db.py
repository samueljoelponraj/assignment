import sqlite3

conn = sqlite3.connect("collegedb.db")
cursor = conn.cursor()

# create student table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    regno INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT
);
""")

# create list of book table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    bookid INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT,
    year INTEGER,
    available INTEGER DEFAULT 1
);
""")

# student test score table
cursor.execute("""
CREATE TABLE IF NOT EXISTS test_scores (
    regno INTEGER PRIMARY KEY,
    english INTEGER,
    tamil INTEGER,
    maths INTEGER,
    science INTEGER,
    social INTEGER,
    FOREIGN KEY (regno) REFERENCES students(regno)
);
""")

# the borrow table book
cursor.execute("""
CREATE TABLE IF NOT EXISTS borrowed_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    regno INTEGER,
    bookid INTEGER,
    date TEXT,
    FOREIGN KEY (regno) REFERENCES students(regno),
    FOREIGN KEY (bookid) REFERENCES books(bookid)
);
""")

conn.commit()
conn.close()

print("All tables created successfully")
