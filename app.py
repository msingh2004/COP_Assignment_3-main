import sqlite3
from flask import Flask, render_template
from werkzeug.exceptions import abort


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

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/byauthor')
def byauthor():
    return render_template('byauthor.html')

@app.route('/searchresults')
def searchresults():
    return render_template('searchresults.html')

@app.route('/trending')
def trending():
    return render_template('trending.html')

@app.route('/<int:postId>')
def viewPost(postId):
    post = getPost(postId)
    comments = getComments(postId)
    return render_template('blogpost.html', posts=post, comments=comments)

# @app.route('/newpost')
# def newpost()
if __name__ == "__main__":
    app.run(debug=True)
