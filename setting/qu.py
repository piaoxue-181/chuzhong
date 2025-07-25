# -*-coding:utf-8-*-
def q(status):
    # 导入模块
    import json
    import os
    import sqlite3
    from dotenv import load_dotenv

    load_dotenv()

    path_main = os.path.dirname(os.path.abspath('index.py'))
    mode = os.environ.get("MODE")
    item = {'七年级上册': 'qis\\', '七年级下册': 'qix\\', '八年级上册': 'bas\\', '八年级下册': 'bax\\', '九年级上册': 'jius\\', '九年级下册': 'jiux\\'}
    nianji = input('要听写的年级（如七年级上册）：')
    if nianji != "":
        if mode == "json":
            # 用户输入要进行听写的课节，然后从指定的json文件中读取单词列表，并保存在全局变量v中。
            try:
                if os.path.exists(os.path.join(path_main, item[nianji])):
                    unit = input('要听写的单元（如unit1）：')
                    if unit != '':
                        try:
                            if os.path.exists(os.path.join(path_main, item[nianji] + unit + '.json')):
                                with open(os.path.join(path_main, item[nianji] + unit + '.json'), 'r', encoding='UTF-8') as b:
                                    q_a = b.read()
                                    str_q = str(q_a).replace('\n', '')
                                    str_q = str_q.replace('  ', '')
                                webjson = json.loads(str_q)
                                if status == 'True':
                                    topic = input('要听写的话题（如topic1）：')
                                    try:
                                        webjson = webjson['txt'][topic]
                                        return webjson, unit, topic
                                    except:
                                        return 'error', '{} 话题不存在！'.format(topic)
                                else:
                                    return webjson, unit
                            else:
                                return 'error', '有关 {} 的文件不存在！'.format(unit)
                        except:
                            return 'error', '未知'
                    else:
                        return 'error', '单元变量未输入'
                else:
                    return 'error', '有关 {} 的文件夹不存在！'.format(nianji)
            except KeyError:
                return 'error', '有关 {} 的文件夹不存在！'.format(nianji)
    
        else:
            path = os.path.join(path_main, f"word_list\\{item[nianji]}")
            if os.path.exists(path):
                unit = input('要听写的单元（如unit1）：')
                if unit != "":
                    if os.path.exists(os.path.join(path, unit + '.db')):
                        conn = sqlite3.connect(os.path.join(path, unit + '.db'))
                        cursor = conn.cursor()
                        if status == 'True':
                            topic = input("要听写的话题（如topic1）：")
                            if cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{topic}';") != []:
                                cursor.execute(f"select * from {topic}")
                                topic_yuan = cursor.fetchall()
                                topic_json = {}
                                for w in topic_yuan:
                                    topic_json[w[1]] = w[2]
                                return topic_json, unit, topic
                            else:
                                return 'error', '{} 话题不存在！'.format(topic)
                        else:
                            table_names = [row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")]
                            topic_json = {}
                            topic_json["unit"] = table_names
                            topic_json['txt'] = {}
                            for r in table_names:
                                cursor.execute(f"select * from {r}")
                                topic_yuan = cursor.fetchall()
                                topic_json["txt"][r] = {}
                                for p in topic_yuan:
                                    topic_json["txt"][r][p[1]] = p[2]
                            return topic_json, unit
                    else:
                        return 'error', '有关 {} 的文件不存在！'.format(unit)
                else:
                    return 'error', '单元变量未输入'
            else:
                return 'error', '有关 {} 的文件夹不存在！'.format(nianji)
    else:
        return 'error', '年级变量未输入'
