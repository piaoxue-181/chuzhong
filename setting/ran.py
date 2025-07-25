def huan(v):
    import random
    # 将单词列表随机一下
    dict_key_ls = list(v.keys())
    random.shuffle(dict_key_ls)
    new_dic = {}
    for key in dict_key_ls:
        new_dic[key] = v.get(key)
    v = new_dic
    return v
