import sqlite3

conn = sqlite3.connect(r"C:\Users\Administrator\Desktop\main\chuzhong\word_list\bas\unit2.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS review_of_units_1_2 (
    id INTEGER PRIMARY KEY,
    words TEXT,
    chinese TEXT
);""")
conn.commit()