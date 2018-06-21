
import tmall
import user_feature
import user_rule

def getCommadResult():
    data = tmall.loadData()
    feature, feature_name = user_feature.generateFeature('train', data)
    model = tmall.getModelByLogistic(feature, feature_name)
    feature, feature_name = user_feature.generateFeature('predict', data)
    recommend = tmall.getRecommendByLogistic(model, feature, feature_name)
    f = open("./data/result.txt", "r")
    result = []
    lines = f.readlines()
    for index, item in enumerate(lines):
        uid, bid = item.strip("\n").split("\t")
        yiha = set(bid.split(","))
        for i in yiha:
            result.append((uid, i))
    f.close()
    return recommend, result

def getRuleResult():
    data = tmall.loadData()
    recommend = user_rule.getRecommendByRule(data)
    f = open("./data/result.txt", "r")
    result = []
    lines = f.readlines()
    for index, item in enumerate(lines):
        uid, bid = item.strip("\n").split("\t")
        yiha = set(bid.split(","))
        for i in yiha:
            result.append((uid, i))
    f.close()
    return recommend, result
