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


#This function below prevents titles from being the same. 
#eg: if the title "blogpost1" already exists"
#it will become "blogpost1(1)
#and if blogpost1(1) already exists
#it will become blogpost1(2)
#it has been implemented already, and has been tested.

def give_new_title(title,titles): 
    repeat=False
    nums=['0','1','2','3','4','5','6','7','8','9']
    for each in titles:
        if(each==title):
               repeat=True
    if(repeat==False):
        return title
    else:
        if(len(title)>3):
            if(title[-2] in nums and title[-3]=='(' and title[-1]==')'):
                base=ord('0')
                number=ord(title[-2])-base
                title=title[:-3]+"("+str(number+1)+")"
                return give_new_title(title,titles)
            else:
                return give_new_title(title+"(1)",titles);
        else:
            return give_new_title(title+"(1)",titles)

@app.route("/", methods=["GET","POST"])
def home():
    g.conn = get_db()
    c = g.conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS blogs(title text, body text, name text, id INTEGER PRIMARY KEY)")
    c.execute("CREATE TABLE IF NOT EXISTS comments(pid integer, comment text, cname text)")
    g.conn.commit()
    if ('title' in request.form and 'body' in request.form):
        title = request.form['title']
        body = request.form['body']
        name = "Anonymous"
        if ('name' in request.form and request.form['name'] != ""):
            name = request.form['name']
        if(title.replace(" ", "")!="" and body.replace(" ", "")!=""):
            titles=[]
            for each in c.execute('''SELECT title FROM blogs'''):
                titles+=each
            title=give_new_title(title,titles)
            c.execute("INSERT INTO blogs VALUES(?, ?, ?, NULL)", (title, body, name,))
            g.conn.commit()
    
    L = []
    posts = c.execute('''SELECT title FROM blogs ORDER BY title;''')
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
            cname = "Anonymous"
            if ('name' in request.form and request.form['name'] != ""):
                cname = request.form['name']
            if(comment.replace(" ", "")!=""):
                c.execute("insert into comments values(?, ?, ?)", (result[3], comment, cname))
                g.conn.commit()
        title = result[0]
        body = result[1]
        name = result[2]
        comments = c.execute("select comment from comments,blogs where blogs.id == comments.pid and blogs.title == ?", (title,)).fetchall()
        cnames = c.execute("select cname from comments,blogs where blogs.id == comments.pid and blogs.title == ?", (title,)).fetchall()
        return render_template("post.html", title=title, body=body, name=name, comments=[c[0] for c in comments], names=[n[0] for n in cnames])
    else:
        return render_template("failure.html")

if __name__=="__main__":    
    app.debug=True
    app.run(host="0.0.0.0",port=5678)



