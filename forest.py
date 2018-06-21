#coding=utf-8
# 基于逻辑回归的推荐

# 主要有如下几个步骤：
# 1. 加载数据；
# 2. 生成特征；
# 3. 对训练集进行训练，建立推荐模型；
# 4. 将模型应用于验证集，生成推荐结果；
# 5. 对推荐结果进行检验；
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

def getForestData():
    f = open("./data/train.txt", "r")
    x_train = []
    y_train = []
    line = f.readline()
    line = f.readline()
    while line:
        uid, bid, flag, click, buy, fav, cart, diff_day = line.strip().split(',')
        x_train.append((uid, bid, click, fav, cart))
        y_train.append(buy)
        line = f.readline()
    f.close()
    f2 = open("./data/predict_result.txt", "r")
    x_test = []
    y_test = []
    line2 = f2.readline()
    line2 = f2.readline()
    while line2:
        uid, bid, flag, click, buy, fav, cart, diff_day = line2.strip().split(',')
        x_test.append((uid, bid, click, fav, cart))
        y_test.append(buy)
        line2 = f2.readline()
    f2.close()
    clf = RandomForestClassifier(n_jobs=10)
    clf.fit(x_train, y_train)
    prediction = clf.predict(x_test[1:4000])
    return list(prediction), y_test[1:4000]
