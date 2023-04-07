import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.exceptions import abort

IS_SESSION = False

def regex(expr, item):
    reg = re.compile(expr)
    return reg.search(item)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def getPost(postId):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (postId,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def getComments(postId):
    conn = get_db_connection()
    comments = conn.execute('SELECT * FROM comments WHERE post_id = ?', (postId,)).fetchall()
    conn.close()
    if comments is None:
        return {}
    return comments

def getResults(keyword):
    # keyword is a string

    conn = get_db_connection()
    conn.create_function("REGEXP", 2, regex)
    results = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    results_act = []
    for result in results:
        if keyword in result['title']:
            results_act.append(result)
    if getResults is None:
        return {}
    return results_act

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# blogs = [{'author' : 'Nice', 'title' : 'Blog1', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog2', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog3', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog3', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog3', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog', 'text' : "hello"}
# ]
         
@app.route('/')
def home():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html',posts=posts)

# @app.route('/blogpost')
# def blogpost():  
#     return render_template('blogpost.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/signup')
# def signup():
#     return render_template('signup.html')

@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = getResults(keyword)
        return render_template('searchresults.html', results=results)
    else:
        return render_template('search.html')

@app.route('/<string:username>')
def byauthor(username):
    conn = get_db_connection()
    blogs = conn.execute('SELECT * FROM posts WHERE author = ?', (username,)).fetchall()
    return render_template('byauthor.html', username=username, blogs=blogs)
# @app.route('/searchresults')
# def searchresults():
#     return render_template('searchresults.html')

@app.route('/trending')
def trending():
    return render_template('trending.html')

@app.route('/<int:postId>', methods=('GET', 'POST'))
def viewPost(postId):
    post = getPost(postId)
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Can\'t put empty comment')
        else:
            conn = get_db_connection()
            author = session['username']
            conn.execute('INSERT into comments (post_id, content, author) VALUES (?, ?, ?)', (postId, content, author))
            conn.commit()
            conn.close()
            redirect(url_for('home'))
    comments = getComments(postId)
    return render_template('blogpost.html', posts=post, comments=comments)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        author = session['username']
        if not title:
            flash('Title is necessary')
            return redirect('/create')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content, author) VALUES (?, ?, ?)', (title, content, author))
            conn.commit()
            conn.close()
            return redirect('/')
    return render_template('newpost.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    session["username"] = None
    if request.method == 'POST':
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? and pass_key = ?', (request.form["username"], request.form["password"])).fetchone()
        conn.close()
        if user is not None:
            if user['username'] == request.form["username"] and user['pass_key'] == request.form["password"]:
                session["username"] = request.form["username"]
                session["password"] = request.form["password"]
                IS_SESSION = True
                flash("logged in successfully")
                return redirect(url_for('home'))
            else:
                flash("Incorrect username or password")
                return redirect(url_for('login'))
        else:
            flash("Incorrect username or password")
            return redirect(url_for('login'))
    else:
        flash("hello")
        return render_template('login.html')
        
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, pass_key) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/following')
def following():
    return render_template('following.html')

if __name__ == "__main__":
    app.run(debug=True)
