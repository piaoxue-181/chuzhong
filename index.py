import json
import logging
import os
import platform
import re
import sys
from dotenv import load_dotenv

import chardet

import setting.qu as pya
import setting.ran as pyb
import setting.xie as pyc

logger = logging.getLogger(__name__)
load_dotenv()
mode = os.environ.get("MODE")
def print_t(print_py):
    print(print_py)

print('''欢迎来到听写框架组织旗下项目~
程序工作目录：{}
运行程序版本：{}   
组织URL：https://gitcode.com/tingxie'''.format(os.path.dirname(os.path.abspath('index.py')), platform.python_version()))
if mode == "db":
    print("""tips：如要单独听写每个单元最后一个话题，请将空格与“-”全部改为“_”再输入~
""")
    pass
else:
    print("\n")



def cuo():
    """错题复习流程，自动检测桌面 problem.json 并处理。"""
    def search(desktop_path):
        try:
            with open(desktop_path, 'rb') as open_read:
                raw_data = open_read.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding']
            with open(desktop_path, 'r', encoding=encoding) as open_json:
                open_json.seek(0)
                open_json_read = open_json.read().replace('\n', '')
                read_json = json.loads(open_json_read)
                if open_json_read != '{}':
                    return True, read_json
                else:
                    return False, read_json
        except Exception as e:
            logger.error(f"错题文件读取失败: {e}")
            return False, {}

    def xie(read_json):
        yes_xie, no_xie, cuo_a = 0, 0, {}
        for i, ans in read_json.items():
            python = input(f"{i}：")
            if python == 'exit':
                break
            if ',' in ans:
                if python in ans:
                    print_t(f'{python} 对喽~')
                    yes_xie += 1
                else:
                    print_t(f'{python} 错喽错喽！正确答案是：{ans}')
                    no_xie += 1
                    cuo_a[i] = ans
            else:
                if python == ans:
                    print_t(f'{python} 对喽~')
                    yes_xie += 1
                else:
                    print_t(f'{python} 错喽错喽！正确答案是：{ans}')
                    no_xie += 1
                    cuo_a[i] = ans
        print_t('end~\n')
        if no_xie == 0:
            pyc.clean()
        else:
            print_t(f'一共对{yes_xie}个，错{no_xie}个')
            pyc.practice_xie(cuo_a)

    file_name = 'problem.json'
    if 'HOMEPATH' in os.environ:
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', file_name)
    elif 'HOME' in os.environ:
        desktop_path = os.path.join(os.path.expanduser('~/Desktop'), file_name)
    else:
        logger.error("无法确定桌面路径！")
        sys.exit()

    has_problem, problem_json = search(desktop_path)
    if has_problem:
        xie(problem_json)
    else:
        print_t('暂无错题~\n')





# 独立定义ting_main函数，供main_menu调用
def ting_main():
    """主听写流程，支持单元/话题两种模式。"""
    ercuo = {}
    ercuo_count = 0

    def ting(item):
        yes, no = 0, 0
        cuo_a = {}
        for k, v in item.items():
            python = input(f"{v}：")
            if python == 'exit':
                return
            if ',' in k:
                pattern = r"[,]"
                ok = True
                result = re.split(pattern, k)
                for hello in result:
                    if python == hello:
                        print_t('对喽~')
                        yes += 1
                        ok = False
                        break
                if ok:
                    print_t(f'{python}错喽错喽！正确答案为{re.sub(",", "或", k)}~')
                    no += 1
                    cuo_a[v] = k
            else:
                if python == k:
                    print_t('对喽~')
                    yes += 1
                else:
                    print_t(f'{python}错喽错喽！正确答案为{k}~')
                    no += 1
                    cuo_a[v] = k
        print_t('end~\n')
        if no > 0:
            print_t(f'一共对{yes}个，错{no}个')
            print_t(f'不扎实{no}个！巩固错题start~\n')
            gai(cuo_a)

    def gai(item):
        nonlocal ercuo, ercuo_count
        yes_gai, cuocount = 0, 0
        for ttt, ans in item.items():
            python = input(f"{ttt}：")
            if python == 'exit':
                return
            if ',' in ans:
                if python in ans:
                    print_t('对喽~')
                    yes_gai += 1
                else:
                    print_t(f'{python}错喽错喽！正确答案为{re.sub(",", "或", ans)}~')
                    ercuo_count += 1
                    cuocount += 1
                    ercuo[ttt] = ans
            else:
                if python == ans:
                    print_t('对喽~')
                    yes_gai += 1
                else:
                    print_t(f'{python}错喽错喽！正确答案为{ans}~')
                    ercuo_count += 1
                    cuocount += 1
                    ercuo[ttt] = ans
        print_t('end~')
        if yes_gai == 0:
            print_t('内个，全错！\n')
        elif cuocount > 0:
            print_t(f'一共对{yes_gai}个，错{cuocount}个')

    def def_status(status_true_or_false):
        nonlocal ercuo, ercuo_count
        qu = pya.q(status_true_or_false)
        if qu[0] == 'error':
            logger.error(qu[1] if qu[1] != '未知' else '抱歉，系统出现异常情况，程序退出~')
            sys.exit()
        if status_true_or_false == 'False':
            print_t(f'\n第{qu[1].replace("unit", "")}单元~\n')
            qu = qu[0]
            for c in qu['unit']:
                print_t(f'\n第{c.replace("topic", "")}话题~\n')
                item = pyb.huan(qu['txt'][c])
                ting(item)
        else:
            print_t(f'\n第{qu[2].replace("topic", "")}话题~\n')
            item = pyb.huan(qu[0])
            ting(item)
        if ercuo_count != 0:
            print_t(f'\n有{ercuo_count}个二错单词，下面是答案~')
            pyc.index_xie(ercuo)
            ercuo.clear()
            ercuo_count = 0
        print_t('\n')

    status = input('是否以话题为一个单元听写（yes or no）：')
    if status == 'yes':
        def_status('True')
    elif status == 'no' or status == '':
        def_status('False')
    else:
        print_t('我有权怀疑你打错了~\n')


def study():
    # 基础变量设置
    study_count = 0
    study_status = True
    pattern = r'[-]'
    grade = {'七年级上册': 'qis/', '七年级下册': 'qix/', '八年级上册': 'bas/', '八年级下册': 'bax/', '九年级上册': 'jius/', '九年级下册': 'jiux/', '日常练习': 'new_class/'}

    # 获取单词表及话题，起始、结束行数
    get = input('请输入要学习的单词表（例子：七年级上册-unit1）：')
    if get != 'exit' and '-' in get:
        try:
            get_list = re.split(pattern, get)
        except IndexError as a:
            raise IndexError('暴发错误！错误原因：' + str(a))
        if get_list[0] in grade:
            print('年级分类效验完成！~')
            if os.path.exists(grade[get_list[0]] + get_list[1] + '.json'):
                print('单词表效验完成！')
                study_topic = input('学习话题：')
                study_start = input('起始行数：')
                study_end = input('结束行数：')
                if study_topic != 'exit':
                    with open(grade[get_list[0]] + get_list[1] + '.json', 'r', encoding='UTF-8') as read:
                        read.seek(0)
                        json_raed_get = read.read()
                        json_raed_get_py = json.loads(json_raed_get)
                        try:
                            study = json_raed_get_py["txt"][study_topic]
                        except:
                            study = json_raed_get_py

                        print('单词表获取完成！')

                        print_t('开始学习~\n\n')
                        try:
                            if study_start == '':
                                study_start = 1
                            if study_end == '':
                                study_end = 9999999999999999999999999999999999999999999999
                            study_start = int(study_start)
                            study_end = int(study_end)
                            for i in study:
                                study_count += 1
                                if study_count >= study_start and study_count <= study_end:
                                    print('{} -> {}'.format(study[i], i))
                                else:
                                    break
                            print_t('结束~\n\n')
                        except:
                            print_t('话题输出失败！')

            else:
                print_t('暂无此单词表~')

        else:
            print_t('暂无此年级分类~')



# 确保 ting_main 在 main_menu 之前定义

def main_menu():
    """主菜单循环，用户交互入口。"""
    print('-r 练习错题，-p 练习课表，-d 继续学习，-c 关闭进程')
    while True:
        status_input = input('>>>')
        if status_input == '-r':
            cuo()
        elif status_input == '-p':
            ting_main()
        elif status_input == '-d':
            study()
        elif status_input == '-c':
            print_t('进程已关闭。')
            break
        else:
            print_t('未知指令，已退出。')
            break

if __name__ == "__main__":
    main_menu()
    sys.exit()
