"""
author: 末雨乘风(piaoxue-181)
time: 2026/2/15

tips：除夕快乐！
"""

import os
import json

def process_json_to_txt():
    """
    遍历年级目录下的JSON文件，解析并输出为指定格式的TXT文件
    """
    # 定义年级目录（用户指定的缩写）
    grade_dirs = ["qis", "qix", "bas", "bax", "jius", "jiux"]
    # 根目录（JSON文件所在的根路径）
    json_root = "./"
    # TXT输出根目录
    txt_root = "./txt"

    # 遍历每个年级目录
    for grade in grade_dirs:
        grade_json_path = os.path.join(json_root, grade)
        # 检查年级目录是否存在
        if not os.path.isdir(grade_json_path):
            print(f"警告：年级目录 {grade_json_path} 不存在，跳过")
            continue
        
        # 遍历年级目录下的所有JSON文件
        for filename in os.listdir(grade_json_path):
            # 只处理.json文件
            if not filename.endswith(".json"):
                continue
            
            # 提取单元名称（去掉.json后缀）
            unit_name = os.path.splitext(filename)[0]
            # 拼接JSON文件完整路径
            json_file_path = os.path.join(grade_json_path, filename)

            try:
                # 读取并解析JSON文件
                with open(json_file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                
                # 获取txt部分（核心的单词数据）
                txt_data = json_data.get("txt", {})
                if not txt_data:
                    print(f"警告：{json_file_path} 中未找到txt字段，跳过")
                    continue

                # 遍历每个话题（topic）
                for topic, words in txt_data.items():
                    # 构建输出目录路径：./txt/{年级}/{单元}/
                    output_dir = os.path.join(txt_root, grade, unit_name)
                    # 创建目录（如果不存在）
                    os.makedirs(output_dir, exist_ok=True)
                    # 构建TXT文件路径：./txt/{年级}/{单元}/{话题}.txt
                    txt_file_path = os.path.join(output_dir, f"{topic}.txt")

                    # 写入TXT文件
                    with open(txt_file_path, "w", encoding="utf-8") as f:
                        # 遍历每个单词和翻译
                        for word, translation in words.items():
                            # 写入格式：单词 -> 翻译
                            f.write(f"{word} -> {translation}\n")
                            # 每个单词之间空一行
                            f.write("\n")

                print(f"成功处理：{json_file_path}")

            except json.JSONDecodeError:
                print(f"错误：{json_file_path} 不是有效的JSON文件，跳过")
            except Exception as e:
                print(f"错误：处理 {json_file_path} 时发生异常 - {str(e)}")

if __name__ == "__main__":
    # 执行主函数
    process_json_to_txt()
    print("所有文件处理完成！")