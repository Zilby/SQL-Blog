#!/usr/bin/python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
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
