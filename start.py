import sqlite3
import os
import json
import time


path = r"C:\Users\Administrator\Desktop\main\chuzhong"
nianji = "bax"
danyuan_new = "unit2"
danyuan = danyuan_new + ".json"
t_1 = ["topic1", "topic2", "topic3", "review_of_units_5_6"]

new = os.path.join(path, nianji)
path_new = os.path.join(new, danyuan)
yyy = r"C:\Users\Administrator\Desktop\main\chuzhong\word_list\{}\{}.db".format(nianji, danyuan_new)

conn = sqlite3.connect(yyy)
cursor = conn.cursor()
# 启用WAL模式，减少锁冲突
cursor.execute('PRAGMA journal_mode=WAL;')

for t in t_1:
    data = []
    with open(path_new, "rb") as path_new_db:
        path_new_db.seek(0)
        read_json = json.loads(path_new_db.read())["txt"][t]
        for k in read_json:
            r = [k, read_json[k]]
            data.append(r)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {t} (
    id INTEGER PRIMARY KEY,
    words TEXT,
    chinese TEXT
    );""")
    for i in data:
        cursor.execute(f"insert into {t} (words, chinese) values (?, ?)", i)

conn.commit()  # 所有写入后只commit一次
conn.close()