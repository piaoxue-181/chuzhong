from setting import qu

test = qu.q(False)[0]

for key, value in test["txt"].items():
    print("\n" + key + "：\n")
    for a, b in value.items():
        t = ""
        length = len(a.encode('utf-8'))
        # 使用整数除法 //，确保 range 的参数为整数
        for i in range(length // 3):
            t += "__"
        print(b + " => " + t)