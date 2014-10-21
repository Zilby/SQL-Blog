#!/usr/bin/python
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("data.db")
c = conn.cursor()
#q = "create table blogs(title text, body text)"
#c.execute(q)
#conn.commit()

@app.route("/", methods=["GET","POST"])
def home():
    title = request.args.get("title", None)
    body = request.args.get("body", None)
    print title
    if (title != None and body != None):
        print "GOOD"
        q = "INSERT INTO blogs VALUES(%s, %s)" % (title, body)
        c.execute(q)
        conn.commit()
        q = "select * from blogs"
        result = c.execute(q)
        print result
    L = ["One", "two"]
    return render_template("home.html", l = L)
    
"""@app.route("/<name>")
def pages(name = None):
    #index = 
    return render_template()
"""

if __name__=="__main__":
    app.debug=True
    app.run(host="127.0.0.1",port=5000)
    app.run()
