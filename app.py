import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.exceptions import abort
import pymysql
from beackendtest import *
# IS_SESSION = False

# def regex(expr, item):
#     reg = re.compile(expr)
#     return reg.search(item)


# def get_db_connection():
#     connection = pymysql.connect(host='localhost',
#         user='root', 
#         password = "SQL@0304#",
#         db='db1',)
#     # conn.row_factory = pymysql.Row
#     return connection.cursor()

# def get_db_connection2():
#     connection = pymysql.connect(host='localhost',
#         user='root', 
#         password = "SQL@0304#",
#         db='db1',)
#     # conn.row_factory = pymysql.Row
#     return connection
# # def getPost(postId):
# #     conn = get_db_connection()
# #     post = conn.execute('SELECT * FROM posts WHERE id = ?', (postId,)).fetchone()
# #     conn.close()
# #     if post is None:
# #         abort(404)
# #     return post

# def getPost(postId):
#     conn = get_db_connection()
#     conn.execute('SELECT * FROM posts WHERE id = %s', (postId,))
#     post = conn.fetchone()
#     conn.close()
#     if post is None:
#         abort(404)
#     return post

# # def getComments(postId):
# #     conn = get_db_connection()
# #     comments = conn.execute('SELECT * FROM comments WHERE post_id = ?', (postId,)).fetchall()
# #     conn.close()
# #     if comments is None:
# #         return {}
# #     return comments

# def getComments(postId):
#     conn = get_db_connection()
#     conn.execute('SELECT * FROM comments WHERE post_id = %s', (postId,))
#     comments = conn.fetchall()
#     conn.close()
#     if comments is None:
#         return {}
#     return comments

# def getResults(keyword):
#     # keyword is a string

#     conn = get_db_connection()
#     # conn.create_function("REGEXP", 2, regex)
#     conn.execute('SELECT * FROM posts')
#     results = conn.fetchall()
#     conn.close()
#     results_act = []
#     for result in results:
#         if keyword in result[2]:
#             results_act.append(result)
#     if getResults is None:
#         return {}
#     return results_act

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# blogs = [{'author' : 'Nice', 'title' : 'Blog1', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog2', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog3', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog3', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog3', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog', 'text' : "hello"},{'author' : 'Nice', 'title' : 'Blog', 'text' : "hello"}
# ]
         
@app.route('/')
def home():
    conn = get_db_connection()
    conn.execute('SELECT * FROM posts')
    posts = conn.fetchall()
    conn.close()
    return render_template('index.html',posts=posts)


@app.route('/light')
def home_light():
    conn = get_db_connection()
    conn.execute('SELECT * FROM posts')
    posts = conn.fetchall()
    conn.close()
    return render_template('index_light.html',posts=posts)

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
    conn.execute('SELECT * FROM posts WHERE author = %s', (username,))
    blogs = conn.fetchall()
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
    post2 = (post[0],post[1],post[2],post[3],post[4])
    if request.method == 'POST':
        
        if "hindi" in request.form:
            post2 = (post[0],post[1],post[2],translatetext(post[3]),post[4])
        if 'content' in request.form:
            content = request.form['content']
            if not content:
                flash('Can\'t put empty comment')
            else:
                conn1 = get_db_connection2()
                conn = conn1.cursor()
                author = session['username']
                conn.execute('INSERT into comments (post_id, content, author) VALUES (%s, %s, %s)', (postId, content, author))
                conn1.commit()
                conn1.close()
                redirect(url_for('home'))
    comments = getComments(postId)
    return render_template('blogpost.html', posts=post2, comments=comments)

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
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)', (title, content, author))
            conn1.commit()
            conn1.close()
            return redirect('/')
    return render_template('newpost.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    session["username"] = None
    if request.method == 'POST':
        
        conn = get_db_connection()
        conn.execute('SELECT * FROM users WHERE username = %s and pass_key = %s', (request.form["username"], request.form["password"]))
        user = conn.fetchone()
        conn.close()
        if user is not None:
            if user[0] == request.form["username"] and user[1] == request.form["password"]:
                session["username"] = request.form["username"]
                session["password"] = request.form["password"]
                IS_SESSION = True
                flash("Logged in successfully")
                return redirect(url_for('home'))
            else:
                flash("Incorrect username or password")
                return redirect(url_for('login'))
        else:
            flash("Incorrect username or password")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
        
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        conn1 = get_db_connection2()
        conn = conn1.cursor()
        conn.execute('INSERT INTO users (username, pass_key) VALUES (%s, %s)', (username, password))
        conn1.commit()
        conn1.close()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/following')
def following():
    return render_template('following.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
#,host="10.17.51.212",port=5000