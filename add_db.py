import sqlite3
import os
import json
import re

# 根路径（原始字符串避免转义）
root_path = r"C:\Users\blows\Desktop\chuzhong"
# 数据库根目录（固定）
db_root_dir = os.path.join(root_path, "word_list")
json_py = []

# 遍历目录，仅收集json文件（过滤指定目录/文件）
for root, dirs, files in os.walk(root_path, topdown=False):
    for name in files:
        file_path = os.path.join(root, name)
        # 过滤无关路径+仅保留json后缀文件
        if any(key in file_path for key in [".git", "setting", "word_list", "new_class"]):
            continue
        if file_path.endswith(".json"):  # 精准匹配json文件
            json_py.append(file_path)

# 处理每个JSON文件
for full_path in json_py:
    try:
        # ------------------- 核心修改1：提取年级和单元名称 -------------------
        # 计算文件相对根路径的路径（去掉根路径）
        relative_path = full_path.replace(root_path, "").lstrip(os.sep)  # 去掉开头的路径分隔符(\)
        # 拆分：相对路径 = 年级文件夹\单元.json → 拆分为[年级文件夹, 单元.json]
        grade_folder, json_filename = os.path.split(relative_path)
        # 单元名：去掉.json后缀，同时过滤数据库名非法字符
        unit_name = os.path.splitext(json_filename)[0]
        unit_name = re.sub(r"[\\/:*?\"<>|.]", "_", unit_name)  # 数据库名合法过滤
        # 校验：确保提取到年级和单元（防止文件结构错误）
        if not grade_folder or not unit_name:
            raise Exception(f"文件路径结构异常，无法提取年级/单元：{full_path}")

        # ------------------- 核心修改2：构建最终数据库路径并创建年级文件夹 -------------------
        grade_db_dir = os.path.join(db_root_dir, grade_folder)  # word_list\{年级}
        os.makedirs(grade_db_dir, exist_ok=True)  # 动态创建年级子文件夹，已存在则不报错
        db_file = os.path.join(grade_db_dir, f"{unit_name}.db")  # 最终路径：word_list\{年级}\{单元}.db

        # 每个文件独立创建连接，启用WAL模式
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('PRAGMA journal_mode=WAL;')  # 启用WAL减少锁冲突

        # 读取并解析JSON文件
        with open(full_path, "r", encoding="utf-8") as fp:
            r = json.load(fp)

        # 表名合法过滤函数（保留原有逻辑，防止特殊字符）
        def get_legal_table_name(raw_name):
            legal_name = re.sub(r"[^a-zA-Z0-9_]", "", raw_name)
            return legal_name if legal_name else "default_word_table"

        # 校验JSON核心键
        if "txt" not in r:
            raise Exception("JSON文件缺少核心键 'txt'")

        # 创建表（基于txt的key，保留原有容错）
        table_names = r["txt"].keys()
        for raw_table in table_names:
            legal_table = get_legal_table_name(raw_table)
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {legal_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                words TEXT NOT NULL,
                chinese TEXT NOT NULL
            );
            """)

        # 插入数据（保留原有容错，统一表名过滤）
        for raw_key, value in r["txt"].items():
            legal_table = get_legal_table_name(raw_key)
            if not isinstance(value, dict):
                continue
            for words, chinese in value.items():
                cursor.execute(
                    f"INSERT INTO {legal_table} (words, chinese) VALUES (?, ?)",
                    (words, chinese)
                )

        # 提交事务，打印成功信息
        conn.commit()
        print(f"🥝 {full_path} → 烧录至 {db_file} 完成~")

    except Exception as e:
        # 异常回滚，打印失败信息
        if 'conn' in locals():  # 确保conn已定义时才回滚
            conn.rollback()
        print(f"❌ {full_path} 烧录失败：{str(e)}")
    finally:
        # 无论成败，强制关闭连接释放资源
        if 'conn' in locals():
            conn.close()

print(f"🎉 所有JSON文件处理完成！数据库统一存储至：{db_root_dir}")