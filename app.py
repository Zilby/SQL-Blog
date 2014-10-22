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
    c.execute("CREATE TABLE IF NOT EXISTS blogs(title text, body text, id INTEGER PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS comments(pid integer, comment text)")
    g.conn.commit()
    if ('title' in request.form and 'body' in request.form):
        title = request.form['title']
        body = request.form['body']
        c.execute("INSERT INTO blogs VALUES(?, ?, NULL)", (title, body,))
        g.conn.commit()
    
    L = []
    posts = c.execute('''SELECT title FROM blogs 
    ORDER BY title;''')
    for p in posts:
        L.append(p[0])
    g.conn.close()
    return render_template("home.html", l = L)
    
@app.route("/<title>", methods=["GET","POST"])
def pages(title):
    g.conn = get_db()
    c = g.conn.cursor()
    x = c.execute("select * from blogs")
    print x.fetchall()
    x = c.execute("select * from comments")
    print x.fetchall()

    result = c.execute("select * from blogs where title == ?", (title,)).fetchone()
    if (result != None):
        if ('comment' in request.form):
            comment = request.form['comment']
            c.execute("insert into comments values(?, ?)", (result[2], comment,))
            g.conn.commit()
        title = result[0]
        body = result[1]
        comments = c.execute("select comment from comments,blogs where blogs.id == comments.pid and blogs.title == ?", (title,)).fetchall()
        return render_template("post.html", title=title, body=body, comments=[c[0] for c in comments])
    else:
        return render_template("failure.html")

if __name__=="__main__":    
    app.debug=True
    app.run(host="127.0.0.1",port=5678)

