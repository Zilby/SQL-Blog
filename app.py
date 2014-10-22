from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'

#Help from http://flask.pocoo.org/docs/0.10/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('data.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/", methods=["GET","POST"])
def home():
    g.conn = get_db()
    c = g.conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS blogs(title text, body text)")
    g.conn.commit()
    if ('title' in request.form and 'body' in request.form):
        title = request.form['title']
        body = request.form['body']
        q = "INSERT INTO blogs VALUES('%s', '%s')" % (title, body)
        c.execute(q)
        g.conn.commit()
    
    L = []
    posts = c.execute("select title from blogs")
    for p in posts:
        L.append(p[0])
    g.conn.close()
    return render_template("home.html", l = L)
    
@app.route("/<title>")
def pages(title):
    g.conn = get_db()
    c = g.conn.cursor()
    q = "select * from blogs where title == '%s'" % title#.replace("%20", " ")
    result = c.execute(q).fetchone()
    if (result != None):
        title = result[0]
        body = result[1]
        return render_template("post.html", title=title, body=body)
    else:
        return render_template("failure.html")

if __name__=="__main__":    
    app.debug=True
    app.run(host="0.0.0.0",port=5000)

