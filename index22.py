import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template,request
from datetime import datetime, timezone, timedelta

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>張立翰Python網頁1121</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=黃玟瑄>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>張立翰簡介網頁</a><br>"
    homepage += "<a href=/account>表單帳密傳值</a><br>"
    homepage += "<a href=/read>人選人演員查詢</a><br><br>"
    homepage += "<a href=/addbooks>圖書館精選</a><br>"
    homepage += "<a href=/searchbk>圖書查詢</a><br>"
    homepage += "<a href=/spider2>網路爬蟲</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    tz = timezone(timedelta(hours=+8))
    now = datetime.now(tz)
    return render_template("today.html", datetime = str(now))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/read")
def read():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("人選之人─造浪者")    
    docs = collection_ref.get()    
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/addbooks")
def addbooks():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("圖書精選")
    docs = collection_ref.order_by("anniversary").get()   
    for doc in docs:
        bk = doc.to_dict()         
        Result += "書名:<a href=" + bk["url"] + ">" + bk["title"] + "</a><br>"
        Result += "作者:" + bk["author"] + "<br>"
        Result += str(bk["anniversary"]) + "週年<br>"
        Result += "<img src=" + bk["cover"] + "></img><br><br>"

    return Result

@app.route("/searchbk", methods=["GET", "POST"])
def searchbk():
    if request.method == "POST":
        keyword = request.form["keyword"]
        result = "您輸入的書名是：" + keyword
        
        Result = ""
        db = firestore.client()
        collection_ref = db.collection("圖書精選")
        docs = collection_ref.get()   
        for doc in docs:
            bk = doc.to_dict()
            if keyword in bk["title"]:         
                Result += "書名:<a href=" + bk["url"] + ">" + bk["title"] + "</a><br>"
                Result += "作者:" + bk["author"] + "<br>"
                Result += str(bk["anniversary"]) + "週年<br>"
                Result += "<img src=" + bk["cover"] + "> </img><br><br>"
        return Result
    else:
        return render_template("searchbk.html")

@app.route("/spider2")
def spider2():
    url = "https://www1.pu.edu.tw/~tcyang/course.html"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".team-box")
    info = ""
    for x in result:
        info += "<a href=" + x.find("a").get("href") + ">"+ x.text + "<br>"
        info += x.find("a").get("href") + "<br><br>" 
    return info              

#if __name__ == "__main__":
    #app.run(debug=True)
