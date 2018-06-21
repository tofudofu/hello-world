# coding=utf-8
#
# 定义通用函数
#
import time
import datetime
from flask import jsonify
import numpy as np
import pandas as pd
import statsmodels.api as sm

import sys
sys.dont_write_bytecode = True

import warnings
warnings.filterwarnings("ignore")



def anlyeFun(locate):
    f = open("./data/train.txt", "r")
    x_train = []
    y_train = []
    click_set = []
    fav_set = []
    cart_set = []
    line = f.readline()
    line = f.readline()
    while line:
        uid, bid, flag, click, buy, fav, cart, diff_day = line.strip().split(',')
        click_set.append(int(click))
        fav_set.append(int(fav))
        cart_set.append(int(cart))
        x_train.append((click, fav, cart, buy))
        line = f.readline()
    f.close()
    colum = ['click', 'fav', 'cart', 'buy']
    df = pd.DataFrame(x_train, columns=['click', 'fav', 'cart', 'buy'])

    y_train.append(click_set)
    y_train.append(fav_set)
    y_train.append(cart_set)


    for i in range(locate, locate+1):
        data = []
        group = df.groupby(colum[i])
        num = max(y_train[i])+1
        for j in range(0, num):
            if j in y_train[i]:
                print('在啊', j)
                get_j = group.get_group(str(j))
                group_buy = get_j.groupby('buy')
                all = len(get_j)
                train = get_j[get_j['buy']=='0']
                key = len(train)
                if key > 0 :
                    nobuy = len(group_buy.get_group('0'))
                    buy = all-nobuy
                    f = float(buy)/all
                    print(f)
                    data.append((str(j), all, f*100))
                    print(data)

    return data
