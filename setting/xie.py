import json
import chardet
import os

file_name = 'problem.json'
desktop_dir = ''

if 'HOMEPATH' in os.environ:  # Windows
    desktop_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop')
elif 'HOME' in os.environ:  # MacOS and Linux
    desktop_dir = os.path.expanduser('~/Desktop')
else:
    print("无法确定桌面路径")

file_path = os.path.join(desktop_dir, file_name)

try:
    with open(file_path, 'rb') as open_json:
        raw_data = open_json.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding) as open_json:
        try:
            existing_data = json.load(open_json)
        except json.JSONDecodeError:
            existing_data = {}

except FileNotFoundError:
    existing_data = {}


def index_xie(data_to_add):
    for key, value in data_to_add.items():
        print('{} -> {}'.format(key, value))
        if key not in existing_data:
            existing_data[key] = value
    with open(file_path, 'w', encoding='utf-8') as open_json_index:
        json.dump(existing_data, open_json_index, ensure_ascii=False, indent=4)


def practice_xie(data_to_add):
    global existing_data
    existing_data = data_to_add
    for i in existing_data:
        print('{} -> {}'.format(i, existing_data[i]))
    with open(file_path, 'w', encoding='utf-8') as open_json_practice:
        json.dump(existing_data, open_json_practice, ensure_ascii=False, indent=4)


def clean():
    with open(file_path, 'w', encoding='utf-8') as open_json_clean:
        open_json_clean.write('{}')
