import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
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

def getResults(keyword):
    # keyword is a string
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM posts WHERE title = ?', (keyword,)).fetchall()
    conn.close()
    if getResults is None:
        return {}
    return results

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
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

@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = getResults(keyword)
        return render_template('searchresults.html', results=results)
    else:
        return render_template('search.html')

@app.route('/byauthor')
def byauthor():
    return render_template('byauthor.html')

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
            conn.execute('INSERT into comments (post_id, content) VALUES (?, ?)', (postId, content))
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

        if not title:
            flash('Title is necessary')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            
    return render_template('newpost.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/following')
def following():
    return render_template('following.html')

if __name__ == "__main__":
    app.run(debug=True)
