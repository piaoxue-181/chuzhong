"""
import setting.xie as pyc
import os
import json
import chardet
import sys

file_name = 'problem.json'
desktop_dir = ''
if 'HOMEPATH' in os.environ:
    desktop_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop')
elif 'HOME' in os.environ:
    desktop_dir = os.path.expanduser('~/Desktop')
else:
    print("无法确定桌面路径")
    sys.exit()

file = os.path.join(desktop_dir, file_name)

with open(file, 'rb') as open_json:
    open_json.seek(0)
    open_json_read = open_json.read()
    result = chardet.detect(open_json_read)

with open(file, 'r', encoding=result['encoding']) as open_json:
    open_json.seek(0)
    open_json_read = open_json.read()
    str(open_json_read)
    if open_json_read != '{}':
        open_json_read = open_json_read.replace('\n', '')
        read_json = json.loads(open_json_read)
    else:
        print('数据库里啥也没有！')
        sys.exit()
    '''
    for i in read_json:
        print('{} -> {}'.format(i, read_json[i]))
    '''
yes, no, cuo = 0, 0, {}
for i in read_json:
    python = input(i + '：')
    if ',' in read_json[i]:
        if python in read_json[i]:
            print('{} 对喽~'.format(python))
            yes += 1
        else:
            print('{} 错喽错喽！正确答案是：{}'.format(python, read_json[i]))
            no += 1
            cuo[i] = read_json[i]
    else:
        if python == read_json[i]:
            print('{} 对喽~'.format(python))
            yes += 1
        else:
            print('{} 错喽错喽！正确答案是：{}'.format(python, read_json[i]))
            no += 1
            cuo[i] = read_json[i]
print('end~\n')
if no == 0:
    pyc.clean()
else:
    print('一共对' + str(yes) + '个，错' + str(no) + '个')
    pyc.practice_xie(cuo)
"""
"""

import json
import setting.xie as pyc

with open('bas/unit2.json', 'r', encoding='UTF-8') as b:
    q = b.read()
    str_q = str(q).replace('\n', '')
    str_q = str_q.replace('  ', '')
webjson = json.loads(str_q)['txt']['topic2']
count = 1
start = 1
end = 20
yes, no = 0, 0
list_cuo = {}
for i in webjson:
    if count >= start and count <= end:
        print('{} -> {}'.format(i, webjson[i]))
        '''
        u = input('{} -> '.format(webjson[i]))
        if u == i:
            print('pass')
            yes += 1
        else:
            print('{}：错了错了~，正确是：{}'.format(u, i))
            no += 1
            list_cuo[webjson[i]] = i
        '''
        count += 1

    elif count <= end:
        count += 1
        continue

    else:
        break

if no != 0:
    count = 1
    print('\n有 {} 个错题, 总共 {} 个'.format(no, end))
    yes, no = 0, 0
    new_list = list_cuo.copy()
    for i in new_list:
        u = input('{} -> '.format(i))
        if u == i:
            print('pass')
            yes += 1
        else:
            print('{}：错了错了~，正确是：{}'.format(u, new_list[i]))
            no += 1
            list_cuo[i] = new_list[i]
        count += 1

    print('\n有 {} 个错题, 总共 {} 个'.format(no, count))
    pyc.index_xie(list_cuo)
"""
import sqlite3
conn = sqlite3.connect(r"C:\Users\Administrator\Desktop\main\chuzhong\word_list\bas\unit1.db")
cursor = conn.cursor()
table_names = [row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")]
print(table_names)
for tname in table_names:
    cursor.execute(f'SELECT * FROM "{tname}"')
    print(cursor.fetchall())
conn.commit()
conn.close()