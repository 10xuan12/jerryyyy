from flask import Flask, render_template,request
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>黃玟瑄網頁</h1>"
    homepage += "<a href=/myweb>黃玟瑄簡介網頁</a><br>"
    homepage += "<a href=/myweb>MIS相關工作介紹</a><br>"
    homepage += "<a href=/myweb>職涯測驗結果</a><br>"
    homepage += "<a href=/myweb>求職履歷</a><br>"
    return homepage

@app.route("/myweb")
def about():
    return render_template("myweb.html")        
if __name__ == "__main__":
    app.run()
