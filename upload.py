import sqlite3

conn = sqlite3.connect(r"C:\Users\blowswind\Desktop\chuzhong\word_list\bax\unit3.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS topic3 (
    id INTEGER PRIMARY KEY,
    words TEXT,
    chinese TEXT
);""")
conn.commit()