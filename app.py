#!/usr/bin/python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    
"""@app.route("/<name>")
def pages(name = None):
    #index = 
    return render_template()
"""

if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=6000)
    app.run()
