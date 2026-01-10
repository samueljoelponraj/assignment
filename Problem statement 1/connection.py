import sqlite3
def condb():
    Dbcon = "collegedb.db"
    conn = sqlite3.connect(Dbcon)
    conn.row_factory = sqlite3.Row
    return conn