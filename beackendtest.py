import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
from werkzeug.exceptions import abort
import pymysql
import requests
import json
import time
import simpleaudio as sa
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

IS_SESSION = False

def regex(expr, item):
    reg = re.compile(expr)
    return reg.search(item)


def get_db_connection():
    connection = pymysql.connect(host='localhost',
        user='root', 
        password = "Suren@2003",
        db='data1',)
    # conn.row_factory = pymysql.Row
    return connection.cursor()

def get_db_connection2():
    connection = pymysql.connect(host='localhost',
        user='root', 
        password = "Suren@2003",
        db='data1',)
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

def translatetext(post):

    url = "https://microsoft-translator-text.p.rapidapi.com/translate"

    querystring = {"to[0]":"hi","api-version":"3.0","from":"en","profanityAction":"NoAction","textType":"plain"}

    payload = [{ "Text": post }]
    headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "c6109840damshe85ac6c9c87655ep1f5ea4jsnd07fe7d4da69",
	"X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    return (response.text)[27:-15]

def bol_ke_dikha(query):
    url = "https://large-text-to-speech.p.rapidapi.com/tts"

    payload = { "text": query}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "546844ae2emsh072e74a07fb34e2p15afafjsnbb5aa7c8f01b",
        "X-RapidAPI-Host": "large-text-to-speech.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
    id = json.loads(response.text)['id']
    eta = json.loads(response.text)['eta']

    print(f'Waiting {eta} seconds for the job to finish...')
    time.sleep(eta)

    # GET the result from the API
    response = requests.request("GET", url, headers=headers, params={'id': id})
    # if url not returned yet, wait and try again
    while "url" not in json.loads(response.text):
        response = requests.get(url, headers=headers, params={'id': id})
        time.sleep(5)
    # if no error, get url and download the audio file
    if not "error" in json.loads(response.text):
        result_url = json.loads(response.text)['url']
        # download the waw file from results_url
        response = requests.get(result_url)
        # save the waw file to disk
        with open('output.wav', 'wb') as f:
            f.write(response.content)
        print("File output.wav saved!")
        filename = 'output.wav'
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing

    else:
        print(json.loads(response.text)['error'])

def mailing_letter(email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'sonder135246@gmail.com'
    smtp_password = 'bfbdchotvvcvuyys'
    # Set up the email message
    from_address = 'sonder135246@gmail.com'
    subject = 'Welcome to Sonder club !'
    message_template = "Thank you for subscribing to our newsletter. We will keep posting 'top blogs' of on a weekly basis. \n                                                   :)" 
    # Open the Excel file and select the sheet
    # workbook = openpyxl.load_workbook('')
    # sheet = workbook['Sheet1']
    # Extract the data from the sheet
    data = [('User',email)]
    # for row in sheet.iter_rows(min_row=2, values_only=True):
    #     name = row[0]
    #     email = row[1]
    #     data.append((name, email))
    # Connect to the email server
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(smtp_username, smtp_password)
    for name, email in data:
        if name is None or email is None:
            continue
        # Replace the placeholder with the recipient's name
        message = message_template.format(name=name)
        # Create the email message
        msg = MIMEMultipart()
        msg['From']="Sonder"
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        # filename="https://drive.google.com/file/d/1LIF8pJtmLm8vgZHUZUvtx6fZG6qEq5wf/view?usp=share_link"
        # fp=open(filename,'rb')
        # att = MIMEApplication(fp.read(),_subtype="pdf")
        # fp.close()
        # att.add_header('Content-Disposition','attachment',filename='Ankit Mondal CV')
        # msg.attach(att)
        # Send the email
        smtp_connection.sendmail(from_address, email, msg.as_string())
    # Disconnect from the email server
    smtp_connection.quit()

def forgot_password(email,passsword):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'sonder135246@gmail.com'
    smtp_password = 'bfbdchotvvcvuyys'
    # Set up the email message
    from_address = 'sonder135246@gmail.com'
    subject = 'Here is your password'
    message_template = f"Here is your password :    {passsword}\n Have a nice day! :)" 
    # Open the Excel file and select the sheet
    # workbook = openpyxl.load_workbook('')
    # sheet = workbook['Sheet1']
    # Extract the data from the sheet
    data = [('User',email)]
    # for row in sheet.iter_rows(min_row=2, values_only=True):
    #     name = row[0]
    #     email = row[1]
    #     data.append((name, email))
    # Connect to the email server
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(smtp_username, smtp_password)
    for name, email in data:
        if name is None or email is None:
            continue
        # Replace the placeholder with the recipient's name
        message = message_template.format(name=name)
        # Create the email message
        msg = MIMEMultipart()
        msg['From']="Sonder"
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        # filename="https://drive.google.com/file/d/1LIF8pJtmLm8vgZHUZUvtx6fZG6qEq5wf/view?usp=share_link"
        # fp=open(filename,'rb')
        # att = MIMEApplication(fp.read(),_subtype="pdf")
        # fp.close()
        # att.add_header('Content-Disposition','attachment',filename='Ankit Mondal CV')
        # msg.attach(att)
        # Send the email
        smtp_connection.sendmail(from_address, email, msg.as_string())
    # Disconnect from the email server
    smtp_connection.quit()

def askgpt(nice):
    url = "https://chatgpt-api7.p.rapidapi.com/ask"

    payload = { "query": f"summarize \"{nice}\" in approximately 100 words" }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "546844ae2emsh072e74a07fb34e2p15afafjsnbb5aa7c8f01b",
        "X-RapidAPI-Host": "chatgpt-api7.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return (response.json()['response'])