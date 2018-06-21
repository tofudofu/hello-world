# coding=utf-8
# 自定义的推荐规则

from copy import copy
import tmall


# 推荐规则
# 函数可分为两部分
# 1. 计算用户特征
# 2. 根据规则进行筛选
#
# 参数 data: 数组，数组元素为 (user_id, brand_id, action_type, month, day)
# 返回值 R : 数组，数组元素为 (user_id, brand_id)
def getRecommendByRule(data):
    F = {}  # 存储用户特征
    R = []  # 存储推荐结果

    # 所有要进行统计的特征，在这里进行声明并赋予初始值
    item = {
        'click': 0,  # 点击次数
        'fav': 0,  # 加入收藏夹次数
        'cart': 0,  # 加入购物车次数
        'buy': 0,  # 购买次数
        'diff_day': 1000,  # 因为是要推测下一个月的购买情况
    }

    # 1. 计算用户特征
    for uid, bid, action_type, month, day in data:
        # 初始化
        F.setdefault(uid, {})
        F[uid].setdefault(bid, copy(item))

        # 新建一个引用，简化代码
        e = F[uid][bid]

        # 基础特征计算
        if action_type == 0:
            e['click'] += 1
        elif action_type == 1:
            e['buy'] += 1
        elif action_type == 2:
            e['fav'] += 1
        elif action_type == 3:
            e['cart'] += 1

        # 时间特征
        diff_day = tmall.getDiffDay((month, day), (7, 15))
        if diff_day < e['diff_day']:
            e['diff_day'] = diff_day

    # 2. 根据特征进行筛选
    for uid, bid_list in F.items():
        for bid, e in bid_list.items():
            if e['diff_day'] < 30 and (e['click'] > 10 or e['fav'] > 0 or e['cart'] > 0 or e['buy'] > 0):
                R.append((uid, bid))

    return R
