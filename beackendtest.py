import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.exceptions import abort
import pymysql

IS_SESSION = False

def regex(expr, item):
    reg = re.compile(expr)
    return reg.search(item)


def get_db_connection():
    connection = pymysql.connect(host='localhost',
        user='root', 
        password = "Sql@0304#",
        db='db1',)
    # conn.row_factory = pymysql.Row
    return connection.cursor()

def get_db_connection2():
    connection = pymysql.connect(host='localhost',
        user='root', 
        password = "Sql@0304#",
        db='db1',)
    # conn.row_factory = pymysql.Row
    return connection
# def getPost(postId):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM posts WHERE id = ?', (postId,)).fetchone()
#     conn.close()
#     if post is None:
#         abort(404)
#     return post

def getPost(postId):
    conn = get_db_connection()
    conn.execute('SELECT * FROM posts WHERE id = %s', (postId,))
    post = conn.fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# def getComments(postId):
#     conn = get_db_connection()
#     comments = conn.execute('SELECT * FROM comments WHERE post_id = ?', (postId,)).fetchall()
#     conn.close()
#     if comments is None:
#         return {}
#     return comments

def getComments(postId):
    conn = get_db_connection()
    conn.execute('SELECT * FROM comments WHERE post_id = %s', (postId,))
    comments = conn.fetchall()
    conn.close()
    if comments is None:
        return {}
    return comments

def getResults(keyword):
    # keyword is a string

    conn = get_db_connection()
    # conn.create_function("REGEXP", 2, regex)
    conn.execute('SELECT * FROM posts')
    results = conn.fetchall()
    conn.close()
    results_act = []
    for result in results:
        if keyword in result[2]:
            results_act.append(result)
    if getResults is None:
        return {}
    return results_act
