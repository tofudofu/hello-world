# -*- coding: UTF-8 -*-
# app.py
import sqlite3
import pymysql
import tmall
import user_rule, user_feature
import anlye
import forest
import util
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='lobin',
                             db='py')

def query_mysql():
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM weather "
            cursor.execute(sql)
            rv = cursor.fetchall()
            # print(rv)
    finally:
        print(rv)
    return  rv

@app.route("/logic_recommend", methods=["GET"])
def logic2_html():
    return render_template("logic_recommend.html")
@app.route("/logic_recommend_post",methods=["POST"])
def logic2_html_post():
    if request.method == "POST":
        recommend, result = util.getCommadResult()
        tmall.printF1Score(recommend)
        return jsonify(rec=recommend,
                       resu=result)



@app.route("/forest", methods=["GET"])
def forest_html():
    return render_template("forest_get.html")
@app.route("/forest_post",methods=["POST"])
def forest_html_post():
    if request.method == "POST":
        q, p = forest.getForestData()

        return jsonify(mytest=q,
                       myreal=p)

@app.route("/random", methods=["GET"])
def random_html():
    return render_template("random_get.html")
@app.route("/random_post",methods=["POST"])
def random_html_post():
    if request.method == "POST":
        getdata_1 = anlye.anlyeFun(0)
        getdata_2 = anlye.anlyeFun(1)
        getdata_3 = anlye.anlyeFun(2)
        return jsonify(xray=[x[0] for x in getdata_1],
                       num=[x[1] for x in getdata_1],
                       mclick=[x[2] for x in getdata_1],
                       fav=[x[2] for x in getdata_2],
                       mcart=[x[2] for x in getdata_3])

@app.route("/logic", methods=["GET"])
def logic_html():
    return render_template("logic_get.html")

@app.route("/logic_post",methods=["POST"])
def logic_html_post():
    if request.method == "POST":
        data = tmall.loadData()
        feature, feature_name = user_feature.generateFeature('train', data)
        model = tmall.getModelByLogistic(feature, feature_name)
        feature, feature_name = user_feature.generateFeature('predict', data)
        recommend = tmall.getRecommendByLogistic(model, feature, feature_name)
        getdata = tmall.printF1Score(recommend)
        print(getdata)
        return jsonify(numb=[x[0] for x in getdata],
                       pre=[x[1] for x in getdata],
                       re=[x[2] for x in getdata],
                       F1=[x[3] for x in getdata])

@app.route("/rule", methods=["GET"])
def rule_html():
    return render_template("rule_get.html")

@app.route("/rule_post", methods=["post"])
def rule_html_post():
    if request.method == "POST":
        recommend, result = util.getRuleResult()
        tmall.printF1Score(recommend)
        return jsonify(rec=recommend,
                       resu=result)

@app.route("/weather", methods=["GET"])
def weather_get():
    return render_template("weather.html")

@app.route("/weather", methods=["POST"])
def weather():
    if request.method == "POST":
        res = query_mysql()
        print(res)
        return jsonify(month=[x[0] for x in res],
                  evaporate=[x[1] for x in res],
                  rain=[x[2] for x in res])


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)