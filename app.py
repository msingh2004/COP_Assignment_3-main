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

# @app.route('/trending')
# def trending():
#     return render_template('trending.html')


@app.route('/<int:postId>', methods=('GET', 'POST'))
def viewPost(postId):
    post = getPost(postId)
    post2 = (post[0],post[1],post[2],post[3],post[4],post[5],post[6])
    post3 = (post[0],post[1],post[2],post[3],post[4],post[5],post[6])
    if request.method == 'POST':
        
        if "hindi" in request.form:
            post2 = (post[0],post[1],post[2],translatetext(post[3]),post[4], post[5], post[6])
        if "read_aloud" in request.form:
            bol_ke_dikha(post[3])
        if "english" in request.form:
            post2 = post3
        elif "upvote" in request.form:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('SELECT * FROM user_blogs_upvoted WHERE postId = %s', (postId,))
            blog_liked_users = conn.fetchall()
            conn.execute('SELECT * FROM user_blogs_downvoted WHERE postId = %s', (postId,))
            blog_disliked_users = conn.fetchall()
            if (not((session['username'], postId) in blog_liked_users)) and (not((session['username'], postId) in blog_disliked_users)):
                conn.execute('UPDATE posts SET upvotes=upvotes+1 WHERE id = %s', (postId,))
                conn.execute('INSERT into user_blogs_upvoted (username, postId) VALUES (%s, %s)', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost', postId=postId))
            elif (not((session['username'], postId) in blog_liked_users)) and ((session['username'], postId) in blog_disliked_users):
                conn.execute('UPDATE posts SET upvotes=upvotes+1 WHERE id = %s', (postId,))
                conn.execute('UPDATE posts SET downvotes=downvotes-1 WHERE id = %s', (postId,))
                conn.execute('INSERT into user_blogs_upvoted (username, postId) VALUES (%s, %s)', (session['username'], postId))
                conn.execute('DELETE from user_blogs_downvoted WHERE username = %s AND postId = %s', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost', postId=postId))
            else:
                conn.execute('UPDATE posts SET upvotes=upvotes-1 WHERE id = %s', (postId,))
                conn.execute('DELETE from user_blogs_upvoted WHERE username = %s AND postId = %s', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost', postId=postId))
        elif "downvote" in request.form:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('SELECT * FROM user_blogs_upvoted WHERE postId = %s', (postId,))
            blog_liked_users = conn.fetchall()
            conn.execute('SELECT * FROM user_blogs_downvoted WHERE postId = %s', (postId,))
            blog_disliked_users = conn.fetchall()
            if (not((session['username'], postId) in blog_disliked_users)) and (not((session['username'], postId) in blog_liked_users)):
                conn.execute('UPDATE posts SET downvotes=downvotes+1 WHERE id = %s', (postId,))
                conn.execute('INSERT into user_blogs_downvoted (username, postId) VALUES (%s, %s)', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost', postId=postId))

            elif (not((session['username'], postId) in blog_disliked_users)) and ((session['username'], postId) in blog_liked_users):
                conn.execute('UPDATE posts SET downvotes=downvotes+1 WHERE id = %s', (postId,))
                conn.execute('UPDATE posts SET upvotes=upvotes-1 WHERE id = %s', (postId,))
                conn.execute('INSERT into user_blogs_downvoted (username, postId) VALUES (%s, %s)', (session['username'], postId))
                conn.execute('DELETE from user_blogs_upvoted WHERE username = %s AND postId = %s', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost', postId=postId))
            else:
                conn.execute('UPDATE posts SET downvotes=downvotes-1 WHERE id = %s', (postId,))
                conn.execute('DELETE from user_blogs_downvoted WHERE username = %s AND postId = %s', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost', postId=postId))
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
                # redirect(url_for('home'))

        if 'delete' in request.form:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('DELETE from posts WHERE id = %s', (postId,))
            conn1.commit()
            conn1.close()
            return redirect(url_for('home'))
        elif 'delete_comment' in request.form:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('DELETE from comments WHERE comment_id = %s', (request.form['delete_comment'],))
            conn1.commit()
            conn1.close()
            return redirect(url_for('viewPost', postId=postId))
    
    comments = getComments(postId)
    return render_template('blogpost.html', posts=post2, comments=comments)



@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        length = min(len(content),100)
        summary2 = content[0:length-1]
        if "GPT" in request.form:
            summary2 = askgpt(content)
        author = session['username']
        if not title:
            flash('Title is necessary')
            return redirect('/create')
        else:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('INSERT INTO posts (title, content, author,upvotes,downvotes,summary) VALUES (%s, %s, %s,%s,%s,%s)', (title, content, author,0,0,summary2))
            conn1.commit()
            conn1.close()
            return redirect('/')
    return render_template('newpost.html')







    

        
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
                return redirect(url_for('home_light'))
            else:
                flash("Incorrect username or password")
                return redirect(url_for('login'))
        else:
            flash("Incorrect username or password")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/login_light', methods=('GET', 'POST'))
def login_light():
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
                return redirect(url_for('home_light'))
            else:
                flash("Incorrect username or password")
                return redirect(url_for('login_light'))
        else:
            flash("Incorrect username or password")
            return redirect(url_for('login_light'))
    else:
        return render_template('login_light.html')

@app.route('/light')
def home_light():
    conn = get_db_connection()
    conn.execute('SELECT * FROM posts')
    posts = conn.fetchall()
    conn.close()
    return render_template('index_light.html',posts=posts)


@app.route('/signup_light', methods=('GET', 'POST'))
def signup_light():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        conn1 = get_db_connection2()
        conn = conn1.cursor()
        conn.execute('INSERT INTO users (username, pass_key) VALUES (%s, %s)', (username, password))
        conn1.commit()
        conn1.close()
        return redirect(url_for('login_light'))
    else:
        return render_template('signup_light.html')

@app.route('/logout_light')
def logout_light():
    session.pop('username', None)
    return redirect(url_for('home_light'))

@app.route('/following_light')
def following_light():
    return render_template('following_light.html')

@app.route('/forgotpass_light')
def forgotpass_light():
    return render_template('forgotpass_light.html')

@app.route('/profile_light')
def profile_light():
    return render_template('profile_light.html')

@app.route('/create_light', methods=('GET', 'POST'))
def create_light():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        length = min(len(content),100)
        summary2 = content[0:length-1]
        if "GPT" in request.form:
            summary2 = askgpt(content)

        author = session['username']
        if not title:
            flash('Title is necessary')
            return redirect('/create_light')
        else:
            conn1 = get_db_connection2()

            conn = conn1.cursor()
            conn.execute('INSERT INTO posts (title, content, author,upvotes,downvotes,summary) VALUES (%s, %s, %s,%s,%s,%s)', (title, content, author,0,0,summary2))
            conn1.commit()
            conn1.close()
            return redirect('/light')
    return render_template('newpost_light.html')


@app.route('/search_light', methods=('GET', 'POST'))
def search_light():
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = getResults(keyword)
        return render_template('searchresults_light.html', results=results)
    else:
        return render_template('search_light.html')

@app.route('/<string:username>_light')
def byauthor_light(username):
    conn = get_db_connection()
    conn.execute('SELECT * FROM posts WHERE author = %s', (username,))
    blogs = conn.fetchall()
    return render_template('byauthor_light.html', username=username, blogs=blogs)

@app.route('/trending_light')
def trending_light():
    conn1 = get_db_connection2()
    conn = conn1.cursor()
    conn.execute('SELECT * FROM posts')
    posts = list(conn.fetchall())
    posts.sort(key = lambda x : x[5])
    posts.reverse()
    return render_template('trending_light.html', posts=posts)

@app.route('/trending')
def trending():
    conn1 = get_db_connection2()
    conn = conn1.cursor()
    conn.execute('SELECT * FROM posts')
    posts = list(conn.fetchall())
    posts.sort(key = lambda x : x[5])
    posts.reverse()
    return render_template('trending.html', posts=posts)



@app.route('/<int:postId>_light', methods=('GET', 'POST'))
def viewPost_light(postId):
    post = getPost(postId)
    post2 = (post[0],post[1],post[2],post[3],post[4],post[5],post[6])
    post3 = (post[0],post[1],post[2],post[3],post[4],post[5],post[6])
    
    if request.method == 'POST':
        
        if "hindi" in request.form:
            post2 = (post[0],post[1],post[2],translatetext(post[3]),post[4], post[5], post[6])
        if "read_aloud" in request.form:
            bol_ke_dikha(post[3])
        if "english" in request.form:
            post2 = post3

        elif "upvote" in request.form:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('SELECT * FROM user_blogs_upvoted WHERE postId = %s', (postId,))
            blog_liked_users = conn.fetchall()
            conn.execute('SELECT * FROM user_blogs_downvoted WHERE postId = %s', (postId,))
            blog_disliked_users = conn.fetchall()
            if (not((session['username'], postId) in blog_liked_users)) and (not((session['username'], postId) in blog_disliked_users)):
                conn.execute('UPDATE posts SET upvotes=upvotes+1 WHERE id = %s', (postId,))
                conn.execute('INSERT into user_blogs_upvoted (username, postId) VALUES (%s, %s)', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost_light', postId=postId))
            elif (not((session['username'], postId) in blog_liked_users)) and ((session['username'], postId) in blog_disliked_users):
                conn.execute('UPDATE posts SET upvotes=upvotes+1 WHERE id = %s', (postId,))
                conn.execute('UPDATE posts SET downvotes=downvotes-1 WHERE id = %s', (postId,))
                conn.execute('INSERT into user_blogs_upvoted (username, postId) VALUES (%s, %s)', (session['username'], postId))
                conn.execute('DELETE from user_blogs_downvoted WHERE username = %s AND postId = %s', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost_light', postId=postId))
            else:
                conn.execute('UPDATE posts SET upvotes=upvotes-1 WHERE id = %s', (postId,))
                conn.execute('DELETE from user_blogs_upvoted WHERE username = %s AND postId = %s', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost_light', postId=postId))
        elif "downvote" in request.form:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('SELECT * FROM user_blogs_upvoted WHERE postId = %s', (postId,))
            blog_liked_users = conn.fetchall()
            conn.execute('SELECT * FROM user_blogs_downvoted WHERE postId = %s', (postId,))
            blog_disliked_users = conn.fetchall()
            if (not((session['username'], postId) in blog_disliked_users)) and (not((session['username'], postId) in blog_liked_users)):
                conn.execute('UPDATE posts SET downvotes=downvotes+1 WHERE id = %s', (postId,))
                conn.execute('INSERT into user_blogs_downvoted (username, postId) VALUES (%s, %s)', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost_light', postId=postId))

            elif (not((session['username'], postId) in blog_disliked_users)) and ((session['username'], postId) in blog_liked_users):
                conn.execute('UPDATE posts SET downvotes=downvotes+1 WHERE id = %s', (postId,))
                conn.execute('UPDATE posts SET upvotes=upvotes-1 WHERE id = %s', (postId,))
                conn.execute('INSERT into user_blogs_downvoted (username, postId) VALUES (%s, %s)', (session['username'], postId))
                conn.execute('DELETE from user_blogs_upvoted WHERE username = %s AND postId = %s', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost_light', postId=postId))
            else:
                conn.execute('UPDATE posts SET downvotes=downvotes-1 WHERE id = %s', (postId,))
                conn.execute('DELETE from user_blogs_downvoted WHERE username = %s AND postId = %s', (session['username'], postId))
                conn1.commit()
                conn1.close()
                return redirect(url_for('viewPost_light', postId=postId))
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
                # redirect(url_for('home'))

        if 'delete' in request.form:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('DELETE from posts WHERE id = %s', (postId,))
            conn1.commit()
            conn1.close()
            return redirect(url_for('home_light'))
        elif 'delete_comment' in request.form:
            conn1 = get_db_connection2()
            conn = conn1.cursor()
            conn.execute('DELETE from comments WHERE comment_id = %s', (request.form['delete_comment'],))
            conn1.commit()
            conn1.close()
            return redirect(url_for('viewPost_light', postId=postId))
    
    comments = getComments(postId)
    return render_template('blogpost_light.html', posts=post2, comments=comments)



if __name__ == "__main__":
    app.run(debug=True)
#,host="10.17.51.212",port=5000